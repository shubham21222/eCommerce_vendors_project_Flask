from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message  # Import Flask-Mail



app = Flask(__name__, template_folder="template", static_folder='static')
app.secret_key = 'your_secret_key'


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'shubhamraikwar07j@gmail.com'  
app.config['MAIL_PASSWORD'] = 'tgxoijszizjvlqxb'  

mail = Mail(app)  


def send_verification_email(email, verification_code):
    try:
        message = Message('Email Verification', sender='your_email@gmail.com', recipients=[email])
        message.body = f"Your verification code is: {verification_code}"

        mail.send(message)  #

        
    except Exception as e:
        flash('Error sending email: ' + str(e), 'error')
