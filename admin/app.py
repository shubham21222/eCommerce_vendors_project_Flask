from flask import Flask
from admin.admin import admin  # Import the admin Blueprint
from auth import auth    # Import the auth Blueprint
# Other necessary imports

app = Flask(__name__)
# Register the admin and auth Blueprints
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(auth, url_prefix='/auth')

# Other app configurations and routes
