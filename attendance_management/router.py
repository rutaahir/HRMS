from django.conf import settings

class CompanyRouter:
    def _get_db(self):
        """હેલ્પર ફંક્શન: જે સાચો અને ઉપલબ્ધ ડેટાબેઝ રિટર્ન કરશે"""
        from attendance.middleware import ThreadLocal
        db_alias = getattr(ThreadLocal, 'DB_NAME', 'default')

        # 🛡️ જો ડેટાબેઝનું નામ 'settings.DATABASES' માં ના હોય, તો 'default' વાપરો
        # આનાથી 'ConnectionDoesNotExist' એરર ક્યારેય નહીં આવે
        if db_alias not in settings.DATABASES:
            return 'default'
        return db_alias

    def db_for_read(self, model, **hints):
        # Core Django Tables હમેશા Main DB માં જ હોવા જોઈએ
        if model._meta.app_label in ['sessions', 'contenttypes', 'admin', 'auth']:
            return 'default'
            
        # Company મોડેલ હમેશા Main DB માં જ હોય છે
        if model._meta.model_name == 'company':
            return 'default'
            
        return self._get_db()

    def db_for_write(self, model, **hints):
        if model._meta.app_label in ['sessions', 'contenttypes', 'admin', 'auth']:
            return 'default'
            
        if model._meta.model_name == 'company':
            return 'default'
            
        return self._get_db()

    def allow_relation(self, obj1, obj2, **hints):
        # અલગ અલગ ડેટાબેઝ વચ્ચે રિલેશન એલાઉ કરો (Level 0 માટે જરૂરી)
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # અત્યારે બધા જ ડેટાબેઝમાં માઈગ્રેશન એલાઉ કરો
        return True