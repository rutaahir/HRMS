from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile
import random  
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import logout
from attendance.models import Company
from django.contrib.auth.models import Group
from django.db import transaction

from django.db.models import Q
import random
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from attendance.models import Company
import os
from django.core.management import call_command
from django.conf import settings

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import random
from .models import Profile
from attendance.models import Company
from attendance.utils import ensure_db_connection
from attendance.middleware import ThreadLocal

def register_view(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    db_name = f"{company.slug}_db"

    if request.method == "POST":
        # STEP-1: DATA COLLECTION
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        first_name = request.POST.get('first_name', "").strip()
        last_name = request.POST.get('last_name', "").strip()
        phone = request.POST.get("phone", "").strip()

        # STEP-2: BASIC VALIDATION
        if not phone or len(phone) != 10 or not phone.isdigit():
            return render(request, 'accounts/register.html', {'msg': 'Phone number must be exactly 10 digits', 'company': company})

        # Check existence in Main DB
        if User.objects.using('default').filter(username=username).exists():
            return render(request, 'accounts/register.html', {'msg': 'Username already exists', 'company': company})

        if User.objects.using('default').filter(email=email).exists():
            return render(request, 'accounts/register.html', {'msg': 'Email already exists', 'company': company})

        try:
            # 🔥 Ensure the connection to the tenant database is ready
            ensure_db_connection(db_name)

            # 🔥 STEP-3: ATOMIC DUAL-DATABASE SYNC
            with transaction.atomic():
                # A. Create User in DEFAULT DB (For Login Authentication)
                user = User.objects.create_user(
                    username=username, 
                    email=email, 
                    password=password,
                    first_name=first_name, 
                    last_name=last_name
                )
                user.save(using='default')

                # B. Create the SAME User in TENANT DB (To prevent ForeignKey errors)
                # We use the same ID and Password hash to keep them identical
                User.objects.using(db_name).create(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    password=user.password,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    is_active=True
                )

                # C. Group Assignment (Main DB for Auth check)
                group_name = f"{company.slug}_employee"
                group, _ = Group.objects.using('default').get_or_create(name=group_name)
                user.groups.add(group)

                # D. Profile Creation in BOTH DBs
                otp = str(random.randint(100000, 999999))
                
                # Save Profile in Main DB
                Profile.objects.using('default').create(
                    user=user, 
                    otp=otp, 
                    phone=phone, 
                    company=company,
                    is_verified=False, 
                    is_approved=True, 
                    otp_created_at=timezone.now()
                )
                
                # Save Profile in Tenant DB (This fixes your "Profile Not Found" login error)
                Profile.objects.using(db_name).create(
                    user_id=user.id, # Link using ID
                    otp=otp, 
                    phone=phone, 
                    company=company,
                    is_verified=False, 
                    is_approved=True, 
                    otp_created_at=timezone.now()
                )

            # STEP-4: SESSION & EMAIL
            request.session['email'] = email
            subject = "Your OTP Verification Code"
            message = f"Hello {username}, Your OTP is: {otp}"

            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
            except Exception as e:
                print(f"Email error: {e}")

            return redirect('verify_otp', company_slug=company.slug)

        except Exception as e:
            print(f"Registration Error: {e}")
            return render(request, 'accounts/register.html', {'msg': f'System Error: {str(e)}', 'company': company})

    return render(request, 'accounts/register.html', {'company': company})

import random
from django.contrib import messages
from django.contrib.auth.hashers import make_password

# ૧. ઈમેલ સબમિટ કરવા માટે
def forgot_password_view(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    
    if request.method == "POST":
        identifier = request.POST.get("email") 
        
        # ૧. યુઝર શોધો
        user = User.objects.filter(
            (Q(username__iexact=identifier) | Q(email__iexact=identifier)), 
            profile__company=company
        ).last()
        
        if user:
            otp = str(random.randint(100000, 999999))
            # ૨. આ ચોક્કસ યુઝરની પ્રોફાઈલ અપડેટ કરો
            profile = user.profile
            profile.otp = otp
            profile.otp_created_at = timezone.now()
            profile.save()

            # ૩. સેશનમાં ઈમેલને બદલે યુઝર આઈડી (ID) સાચવો - આ વધુ સેફ છે
            request.session['reset_user_id'] = user.id
            
            try:
                send_mail(
                    "Password Reset OTP",
                    f"Hi {user.username}, Your OTP is: {otp}",
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )
                return redirect('verify_reset_otp', company_slug=company.slug)
            except Exception as e:
                messages.error(request, "Error sending email.")
        else:
            messages.error(request, "Wrong Email or Username.")
    
    return render(request, 'accounts/forgot_password.html', {'company_slug': company_slug})

from django.http import JsonResponse
from .models import Profile

from django.db.models import Q

def check_username_exists(request):
    # 'username' પેરામીટરમાં યુઝરનેમ અથવા ઈમેલ હોઈ શકે છે
    identifier = request.GET.get('username', '').strip()
    company_slug = request.GET.get('company_slug', None)
    
    if not identifier or not company_slug:
        return JsonResponse({'is_taken': False})

    # ✅ લોજિક: યુઝરનેમ અથવા ઈમેલ બંનેમાંથી કોઈ પણ એક મેચ થવું જોઈએ
    is_valid = Profile.objects.filter(
        (Q(user__username__iexact=identifier) | Q(user__email__iexact=identifier)),
        company__slug=company_slug
    ).exists()
    
    return JsonResponse({'is_taken': is_valid})

# ૨. OTP વેરિફિકેશન માટે
def verify_reset_otp_view(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    
    if request.method == "POST":
        otp_entered = request.POST.get("otp", "").strip()
        user_id = request.session.get("reset_user_id") # ID મેળવો

        if not user_id:
            messages.error(request, "Session expired. Try again.")
            return redirect('forgot_password', company_slug=company.slug)

        # સીધું User ID અને Company થી પ્રોફાઈલ શોધો
        profile = Profile.objects.filter(user_id=user_id, company=company).first()

        if profile:
            # 🛑 ટર્મિનલમાં આ ચોક્કસ ચેક કરો:
            print(f"--- OTP DEBUG ---")
            print(f"User: {profile.user.username}")
            print(f"DB OTP: '{profile.otp}'")
            print(f"Entered: '{otp_entered}'")
            print(f"------------------")

            if str(profile.otp) == str(otp_entered): # બંનેને સ્ટ્રિંગમાં ફેરવીને સરખાવો
                messages.success(request, "OTP Verified!")
                return redirect('set_new_password', company_slug=company_slug)
            else:
                messages.error(request, "Invalid OTP. Please check the code again.")
        else:
            messages.error(request, "User profile not found.")

    return render(request, 'accounts/verify_reset_otp.html', {'company_slug': company_slug})

# ૩. નવો પાસવર્ડ સેટ કરવા માટે
def set_new_password_view(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    
    if request.method == "POST":
        new_pw = request.POST.get("password")
        # 💡 reset_user_id (ID) vaparvu vadhare safe che jem aapne verify_otp ma karyu
        user_id = request.session.get("reset_user_id")
        
        if not user_id:
            messages.error(request, "Session expired. Please start again.")
            return redirect('forgot_password', company_slug=company.slug)

        user = User.objects.filter(id=user_id).first()
        
        if user:
            user.set_password(new_pw)
            user.save()
            
            # 🔥 CRITICAL STEP: Password set thaya pachi session saf karo
            if 'reset_user_id' in request.session:
                del request.session['reset_user_id']
            if 'reset_email' in request.session:
                del request.session['reset_email']
            
            messages.success(request, "Password reset successfully! Please login.")
            
            # 🚀 Have aa line khub j mahatv ni che:
            # Login page par redirect karo pan company_slug sathe
            return redirect('login', company_slug=company.slug)
        else:
            messages.error(request, "User not found.")
            
    return render(request, 'accounts/set_new_password.html', {'company_slug': company_slug})


def verify_view(request, company_slug):
    if request.method == "POST":
        otp_entered = request.POST.get("otp") # read OTP value from form 
        email = request.session.get("email") # get mail from session ( registration)

        if not email:
            return render(request,'accounts/verify.html',{
                "msg":"Session expired. Try again",
                "company_slug": company_slug

            })
        try:
            # it choose last user with same email
            user = User.objects.filter(email=email).last() # fetch mail user from table 
        except User.DoesNotExist:
            return render(request, 'accounts/verify.html',{
                "msg":"User not found ",
                "company_slug": company_slug
            })

        
        
        user_profile = Profile.objects.get(user=user) # get users profile table's name


        from django.utils import timezone
        from datetime import timedelta

# OTP expiry check
        
        expiry_time = user_profile.otp_created_at + timedelta(minutes=5)

        if timezone.now() > expiry_time:
            return render(request, 'accounts/verify.html',{
                "msg":"OTP Expired!! ",
                "company_slug": company_slug
            })

        if user_profile.otp == otp_entered: # otp compare 
            user_profile.is_verified = True
            user_profile.save()
            return redirect('login', company_slug=company_slug)
        else:
            return render(request, 'accounts/verify.html',{"msg":"Invalid OTP","company_slug": company_slug})
          
    return render(request,'accounts/verify.html',{"company_slug": company_slug})

# accounts/views.py માં login_view સુધારો

from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404

# @transaction.non_atomic_requests
# accounts/views.py

# accounts/views.py

def login_view(request, company_slug=None):
    # Debug info in terminal
    print(f"--- Login Attempt for Slug: {company_slug} ---")

    if not company_slug or company_slug == "default":
        db_alias = 'default'
    else:
        db_alias = f"{company_slug}_db"

    try:
        ensure_db_connection(db_alias)
        ThreadLocal.DB_NAME = db_alias
    except Exception as e:
        print(f"❌ DB Connection Error: {e}")
        db_alias = 'default'

    if request.method == "POST":
        identifier = request.POST.get("username")
        password = request.POST.get("password")

        # 1. Authenticate against Main DB
        user_obj = User.objects.using('default').filter(
            Q(username__iexact=identifier) | Q(email__iexact=identifier)
        ).first()

        if user_obj:
            user = authenticate(request, username=user_obj.username, password=password)
            
            if user:
                print(f"✅ User {user.username} Authenticated!")
                
                if user.is_superuser:
                    login(request, user)
                    return redirect("/attendance/dashboard/superadmin/")

                # 2. Fetch Profile from Main DB to act as the Source of Truth
                try:
                    profile = Profile.objects.using('default').select_related('company').get(user=user)
                    print(f"✅ Profile found. Assigned to: {profile.company.slug if profile.company else 'None'}")
                    
                    # 🔥 THE MASTER FIX: Strict Company Boundary Check 🔥
                    if not profile.company or profile.company.slug != company_slug:
                        print(f"❌ SECURITY BLOCK: User {user.username} attempted to log into {company_slug}, but belongs to {profile.company.slug}")
                        return render(request, "accounts/login.html", {
                            "msg": f"Access Denied. You do not belong to the '{company_slug}' portal.", 
                            "company_slug": company_slug
                        })
                    
                    # 3. Check HR Approval Status
                    if not profile.is_approved:
                        print("❌ User not approved")
                        return render(request, "accounts/login.html", {"msg": "Pending HR approval", "company_slug": company_slug})

                    # 4. Success - Log them in
                    login(request, user)
                    request.session['company_slug'] = company_slug
                    print(f"🚀 Redirecting to Dashboard...")
                    return redirect('dashboard')

                except Profile.DoesNotExist:
                    print(f"❌ ERROR: User exists in Main DB, but NO PROFILE found.")
                    return render(request, "accounts/login.html", {"msg": "Profile missing or not set up.", "company_slug": company_slug})
        
        print("❌ Invalid Credentials")
        return render(request, "accounts/login.html", {"msg": "Invalid email or password.", "company_slug": company_slug})

    return render(request, "accounts/login.html", {"company_slug": company_slug})
def resend_otp_view(request,company_slug):
    email = request.session.get("email")
    user = User.objects.filter(email=email).last()
    user_profile = Profile.objects.get(user=user)
    otp = str(random.randint(100000,999999))
    user_profile.otp = otp
    user_profile.otp_created_at=timezone.now()
    user_profile.save()  

    subject="Your new OTP code "
    message = f"Your new code is : {otp}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject,message,email_from,recipient_list)

    return render(request,'accounts/verify.html',{
        "msg":"New OTP Sent to Your Email",
        "company_slug": company_slug
    })

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    # 1. લોગઆઉટ કરતા પહેલા કંપની સ્લગ મેળવી લો
    slug = None
    if request.user.is_authenticated:
        try:
            # જો યુઝર પાસે પ્રોફાઈલ અને કંપની હોય
            slug = request.user.profile.company.slug
        except:
            pass # જો સુપર એડમિન હોય અથવા પ્રોફાઈલ ના હોય
            
    # 2. લોગઆઉટ કરો
    logout(request)
    
    # 3. યોગ્ય જગ્યાએ રીડાયરેક્ટ કરો
    if slug:
        # જો કંપની મળી હોય તો તેના લોગિન પેજ પર
        return redirect('login', company_slug=slug)
    else:
        # જો કંપની ના મળે (દા.ત. સુપર એડમિન), તો ડિફોલ્ટ એડમિન પેજ પર
        return redirect('/admin/')
    
    
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from attendance.models import Company

def create_dynamic_role(request):
    companies = Company.objects.all()
    # Aapde fakhata attendance app ni permissions batavishu
    permissions = Permission.objects.filter(content_type__app_label='attendance')

    if request.method == "POST":
        company_id = request.POST.get('company')
        role_name = request.POST.get('role_name')
        selected_perms = request.POST.getlist('permissions') # list of permission IDs

        company = Company.objects.get(id=company_id)
        
        # 1. Unique Group Name banavo (CompanySlug_RoleName)
        group_name = f"{company.slug}_{role_name.lower()}"
        
        # 2. Group create karo
        new_group, created = Group.objects.get_or_create(name=group_name)

        # 3. Permissions assign karo
        # if selected_perms:
        #     new_group.permissions.set(selected_perms)
        #     new_group.save()

        return redirect('/attendance/dashboard/superadmin/') # pachi dashboard par mokli do

    return render(request, 'accounts/create_role.html', {
        'companies': companies,
        'permissions': permissions
    })