from .models import Notification

def notification_count(request):
    if request.user.is_authenticated:
        return {
            "unread_count": Notification.objects.filter(
                user=request.user,
                is_read=False
            ).count()
        }
    return {}


from .models import Notification

def notification_count(request):
    if request.user.is_authenticated:
        # 🔥 FIX: Variable name 'my_alerts' rakhyu che (Conflicts rokva mate)
        my_alerts = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
        
        return {
            'my_alerts': my_alerts,  # ✅ Hav 'my_alerts' waprisu
            'unread_count': my_alerts.count()
        }
    return {
        'my_alerts': [],
        'unread_count': 0
    }