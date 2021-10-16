from django.apps import AppConfig


class KakeiboConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kakeibo'

"""
    def ready(self):
       
       This function is called when startup.
       
       from .views import start # <= さっき作った start関数をインポート
       start()

"""