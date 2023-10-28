from flask import Blueprint

admin = Blueprint('admin', __name__, template_folder="templates")

# Import your route functions here
from .admin import admin_dashboard, admin_login

from flask import Blueprint

# Import the admin Blueprint from admin_routes.py
from .admin import admin

# Register the admin Blueprint
def init_app(app):
    app.register_blueprint(admin, url_prefix='/admin')

