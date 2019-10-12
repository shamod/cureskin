import logging

# DEBUG can only be set to True in a development environment for security reasons
DEBUG = False

# Flask Debug ToolBar Settings
DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True
DEBUG_TB_PROFILER_ENABLED = True
DEBUG_TB_INTERCEPT_REDIRECTS = False

# Secret key for generating tokens
SECRET_KEY = 'houdini'

# Admin credentials
ADMIN_CREDENTIALS = ('admin', 'pa$$word')

# Database choice
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Configuration of a Gmail account for sending mails
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'flask.boilerplate'
MAIL_PASSWORD = 'flaskboilerplate123'
ADMINS = ['flask.boilerplate@gmail.com']

# Number of times a password is hashed
BCRYPT_LOG_ROUNDS = 12

# Log Setup
TIMEZONE = 'Europe/Paris'
LOG_LEVEL = logging.DEBUG
LOG_STDOUT = True
LOG_FILENAME = 'activity.log'
LOG_MAXBYTES = 100000
LOG_BACKUPS = 2

# Stripe API Settings
STRIPE_SECRET_KEY = 'sk_test_GvpPOs0XFxeP0fQiWMmk6HYe'
STRIPE_PUBLIC_KEY = 'pk_test_UU62FhsIB6457uPiUX6mJS5x'


