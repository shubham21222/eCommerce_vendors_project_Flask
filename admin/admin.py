from flask import Blueprint, render_template, flash, redirect, url_for, session, request
import pymysql
import bcrypt

MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DB = 'ecommarce'  

db = pymysql.connect(
    host=MYSQL_HOST, port=MYSQL_PORT,
    user=MYSQL_USER, password=MYSQL_PASSWORD,
    db=MYSQL_DB, cursorclass=pymysql.cursors.DictCursor
)

admin = Blueprint('admin', __name__, template_folder="templates")


@admin.route('/admin_dashboard')
def admin_dashboard():
    if 'is_admin' in session:  # Check for the 'is_admin' key in session
        cursor = db.cursor()
        
        # Retrieve all vendor data
        cursor.execute("SELECT * FROM users WHERE role = 'vendor'")
        vendors = cursor.fetchall()
        
        # Retrieve all products from vendors
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        
        cursor.close()

        return render_template('admin_dashboard.html', vendors=vendors, products=products)
    else:
        flash('Login required to access the admin dashboard.', 'error')
        return redirect(url_for('admin.admin_login'))
    

@admin.route('/admin1')
def admin_home():
    return render_template('admin_login.html')


@admin.route('/admin_login/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor()
        query = "SELECT username, password FROM admin_credentials WHERE username = %s"
        cursor.execute(query, (username,))
        admin_data = cursor.fetchone()
        cursor.close()

        if admin_data and bcrypt.checkpw(password.encode('utf-8'), admin_data['password'].encode('utf-8')):
            # Admin authentication successful
            session['is_admin'] = True
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('admin_login.html')

