
DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "bbbdc9a5-aa01-4333-9faf-ec3d7da04ced2ffc5671-ccd4-49d0-9b29-22f70d9cef61738e3342-5f53-4b0e-a2f9-8a77d7f51b84"
NEVERCACHE_KEY = "a3d578da-3f24-4536-a588-4017dcc0cdaf55a689bb-0ff7-4984-9af5-352a536fa3c859469b42-0579-4665-9b9c-6f2324419372"

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.sqlite3",
        # DB name or path to database file if using sqlite3.
        "NAME": "dev.db",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}
