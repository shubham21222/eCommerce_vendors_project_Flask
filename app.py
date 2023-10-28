from flask import Flask, render_template
from flask_mail import Mail
from auth import auth  
#from admin import admin as admin_blueprint, init_app as init_admin_app

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config.from_object('config.ProductionConfig')

#init_admin_app(app)
mail = Mail(app)

app.register_blueprint(auth, url_prefix='/auth')
#app.register_blueprint(admin_blueprint, url_prefix='/admin', name='admin_blueprint')

app.config['SESSION_COOKIE_SECURE'] = False

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

