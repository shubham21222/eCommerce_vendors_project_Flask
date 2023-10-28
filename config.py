import os

class Config:
    # Secret key for session management (change this to a random, secure value)
    SECRET_KEY = 'your_secret_key'

    # Flask-Mail configuration for sending emails
    MAIL_SERVER = 'smtp.example.com'  # SMTP server (e.g., Gmail SMTP)
    MAIL_PORT = 587  # Port for sending mail (587 for TLS)
    MAIL_USE_TLS = True  # Use TLS for secure communication
    MAIL_USE_SSL = False  # Use SSL (if TLS is not available)
    MAIL_USERNAME = 'shubhamraikwar07j@gmail.com'  # Your email username
    MAIL_PASSWORD = 'tgxoijszizjvlqxb'  # Your email password

    # Database configuration (modify with your pymysql connection details)
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'ecommarce'
    MYSQL_UNIX_SOCKET = "/var/run/mysqld/mysqlx.sock"
    # Upload folder for file uploads (modify as needed)
    UPLOAD_FOLDER = 'uploads'

    # Session configuration
    SESSION_COOKIE_SECURE = False  # Set to True for HTTPS environments
    SESSION_COOKIE_HTTPONLY = True  # Restrict JavaScript access to cookies

    # Enable or disable debugging (set to False in production)
    DEBUG = True

    # Flask-WTF CSRF token configuration
    WTF_CSRF_ENABLED = True

    # Application root directory
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True  # Set to True for HTTPS environments

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    # Modify this for testing with pymysql
    MYSQL_DB = 'ecommarce'
