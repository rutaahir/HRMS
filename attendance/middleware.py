import threading

class ThreadLocalManager:
    _storage = threading.local()

    @property
    def DB_NAME(self):
        # ડિફોલ્ટ 'default' રિટર્ન કરશે જો કશું સેટ ના હોય
        return getattr(self._storage, 'db_name', 'default')

    @DB_NAME.setter
    def DB_NAME(self, value):
        self._storage.db_name = value

# ઓબ્જેક્ટ બનાવો જેથી પ્રોજેક્ટમાં ગમે ત્યાં વાપરી શકાય
ThreadLocal = ThreadLocalManager()

class CompanyDatabaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URL ના ભાગ કરો
        path_parts = request.path.strip('/').split('/')
        
        db_to_set = 'default'
        
        # 🛡️ ડેટાબેઝ નક્કી કરવાનું લોજિક
        if 'accounts' in path_parts:
            idx = path_parts.index('accounts')
            # જો accounts પછી કોઈ શબ્દ હોય (દા.ત. accounts/g8/login)
            if len(path_parts) > idx + 1:
                slug = path_parts[idx + 1]
                
                # 🚫 આ શબ્દો ક્યારેય ડેટાબેઝના નામ ના હોઈ શકે
                excluded = [
                    'login', 'logout', 'register', 'profile', 
                    'verify', 'verify-reset-otp', 'forgot-password', 
                    'ajax', 'admin', 'static', 'media'
                ]
                
                if slug not in excluded:
                    db_to_set = f"{slug}_db"

        # ThreadLocal માં વેલ્યુ સેટ કરો
        ThreadLocal.DB_NAME = db_to_set
        
        # ટર્મિનલમાં ચેક કરવા માટે (તમે આ લાઈન પછી કાઢી શકો છો)
        # print(f"DEBUG: Request Path: {request.path} -> Selected DB: {ThreadLocal.DB_NAME}")

        response = self.get_response(request)
        return response