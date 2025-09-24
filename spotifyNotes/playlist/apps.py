from django.apps import AppConfig


class SnConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'playlist'
    
    def ready(self):
        try:
            from playlist.db.db_queries import create_table
            create_table()
        except Exception as e:
            print("db table creation error")
