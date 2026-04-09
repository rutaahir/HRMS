from datetime import timedelta
from django.utils import timezone
from .models import Leave, Holiday


def validate_leave_dates(user, from_date, to_date):

    today = timezone.localdate()

    # 1️⃣ Past date not allowed
    if from_date < today:
        return "Past dates are not allowed"

    # 2️⃣ From > To
    if from_date > to_date:
        return "From date cannot be greater than To date"

    # 3️⃣ Overlapping approved / pending leaves
    existing = Leave.objects.filter(
        user=user,
        status__in=["PENDING", "APPROVED"],
        from_date__lte=to_date,
        to_date__gte=from_date
    )

    if existing.exists():
        return "Leave already applied for selected dates"

    # 4️⃣ Check if ALL days are weekend / holiday
    holidays = set(
        Holiday.objects.values_list("date", flat=True)
    )

    current = from_date
    valid_day_found = False

    while current <= to_date:

        # weekday(): 5=Saturday, 6=Sunday
        if current.weekday() not in [5, 6] and current not in holidays:
            valid_day_found = True
            break

        current += timedelta(days=1)

    if not valid_day_found:
        return "Leave not allowed only on weekends / holidays"

    return None   # ✅ validation passed


from django.db import connection, connections
from django.core.management import call_command
from django.conf import settings

def create_company_database(company_slug):
    db_name = f"{company_slug}_db"
    # 1. Pehla MySQL ma database create karo
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE {db_name} CHARACTER SET utf8 COLLATE utf8_general_ci;")

    # 2. Settings ma dynamic add karo
    new_db_settings = settings.DATABASES['default'].copy()
    new_db_settings['NAME'] = db_name
    settings.DATABASES[db_name] = new_db_settings

    # 3. Tables banavo (Migrate karo)
    call_command('migrate', database=db_name)
# attendance/utils.py માં ઉમેરો
from django.db import connections
from django.conf import settings

def ensure_db_connection(db_name):
    """
    Checks if the database connection exists in Django's runtime.
    If not, it adds it dynamically using the default settings.
    """
    if db_name not in connections:
        # Get the template from your default database settings
        new_db = settings.DATABASES['default'].copy()
        new_db['NAME'] = db_name  # Set the name to 'test2_db'
        
        # Inject it into Django's runtime connections
        settings.DATABASES[db_name] = new_db
        connections.databases[db_name] = new_db
    
    # Try to connect to verify it actually exists in MySQL
    try:
        connections[db_name].cursor()
    except Exception as e:
        print(f"Database {db_name} does not exist on the SQL server: {e}")
        return False
    return True

import threading

thread_local = threading.local()

def set_db_for_request(db_name):
    thread_local.DB = db_name

def get_current_db():
    # જો કોઈ DB સેટ ના હોય તો 'default' વાપરો
    return getattr(thread_local, 'DB', 'default')