from flask import Blueprint, render_template, redirect, url_for, request, flash, session ,get_flashed_messages
import pymysql
import bcrypt
import random
import string
from email_verification import send_verification_email
from flask_mail import Mail, Message

auth = Blueprint('auth', __name__,template_folder="templates")


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

@auth.route('/')
@auth.route('/login/')


@auth.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        full_name = request.form.get('fname')
        mobile_number = request.form.get('lname')
        description = request.form.get('product_detail')

        # Server-side validation
        if len(full_name) > 20:
            flash('Full name exceeds the maximum length of 20 characters.', 'error')

        if len(mobile_number) > 12:
            flash('Mobile number exceeds the maximum length of 12 characters.', 'error')

        if len(description) > 100:
            flash('Product description exceeds the maximum length of 100 characters.', 'error')

        if not any(error[1] == 'error' for error in get_flashed_messages()):
            try:
                cursor = db.cursor()
                insert_query = "INSERT INTO contact_form_data (full_name, mobile_number, description) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (full_name, mobile_number, description))
                db.commit()
                cursor.close()

                flash('Your message has been submitted successfully!', 'success')
            except Exception as e:
                db.rollback()
                print("Database Error:", str(e))
                flash('An error occurred while submitting your message. Please try again later.', 'error')

    return render_template('home.html')



@auth.route('/registration/')
def home1():
    return render_template('vendor_registration.html')


@auth.route('/submit', methods=['POST'])
def submit():
    input_value = request.form['shubh']  # Get the input value (username or email)
    password = request.form['password']

    cursor = db.cursor()
    
    # Check if the input value is an email address
    if '@' in input_value:
        query = "SELECT username, password, email, is_verified FROM users WHERE email = %s"
        error_message = 'Incorrect email or password'
    else:
        query = "SELECT username, password, email, is_verified FROM users WHERE username = %s"
        error_message = 'Incorrect username or password'

    cursor.execute(query, (input_value,))
    user_data = cursor.fetchone()

    if user_data:
        stored_password = user_data['password']
        email = user_data['email']
        is_verified = user_data['is_verified']

        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            session['email'] = email 
            cursor.close()

            if is_verified:
                # User has completed the onboarding process, redirect to product_details
                return redirect(url_for('auth.product_details'))
            else:
                # User has not completed the onboarding process, show a message
                flash('Registration not completed. Please complete the registration process.', 'error')
                return redirect(url_for('auth.home1'))
        else:
            flash(error_message, 'error')
    else:
        flash(error_message, 'error')
    cursor.close()
    
    # Redirect to the login page
    return redirect(url_for('auth.home1'))


@auth.route('/register/')
def register_form():
    return render_template('register.html')

@auth.route('/register', methods=['POST'])
def register():
    try:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        product_detail = request.form['product_detail']
        username = request.form['username']
        password = request.form['password']
        session['email'] = email
        session['username'] = username
        cursor = db.cursor()
        query = "SELECT username FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        existing_username = cursor.fetchone()

        if existing_username:
            # flash('Username is already taken. Please choose a different one.', 'error')
            return render_template('register.html')
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            query = "INSERT INTO users (username, password, first_name, last_name, email, address, city, state, product_detail, is_verified) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (username, hashed_password, first_name, last_name, email, address, city, state, product_detail, False))

            db.commit()

            verification_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            cursor.execute("INSERT INTO email_verification (email, verification_code) VALUES (%s, %s)", (email, verification_code))
            db.commit()

            send_verification_email(email, verification_code)

            flash('Registration successful. Please check your email to verify your address.', 'success')
        return redirect(url_for('auth.verify_email_form', email=email))
    except Exception as e:
        flash('Error: ' + str(e), 'error')

    return render_template('register.html')

@auth.route('/registration_form', methods=['GET'])
def registration_form():
    username = session.get('username')

    return render_template('registration.html',username=username)

@auth.route('/on_board_registration', methods=['POST'])
def register1():
    try:
        username = session.get('username')
        email = session.get('email')
        item_name = request.form['item_name']
        listing = request.form['listing']
        stock = request.form['stock']
        pickup_address = request.form['pickup_address']
        pickup_pincode = request.form['pickup_pincode']
        bank_account = request.form['bank_account']
        ifsc_code = request.form['ifsc_code']

        cursor = db.cursor()
        
        # Define the SQL query to insert data into the 'onboarding_registration' table
        insert_query = "INSERT INTO onboarding_registration (email, item_name, listing, stock, pickup_address, pickup_pincode, bank_account, ifsc_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        
        # Execute the query with the provided data
        cursor.execute(insert_query, (email, item_name, listing, stock, pickup_address, pickup_pincode, bank_account, ifsc_code))
        
        # Commit the changes to the database
        db.commit()
        
        # Close the cursor
        cursor.close()

        # Redirect to a success page or perform other actions as needed
        return render_template('success.html',username = username)
    
    except Exception as e:
        # Handle any exceptions that occur during the insertion process
        flash('Error: ' + str(e), 'error')
        return redirect(url_for('auth.registration_form'))




@auth.route('/verify_email_form', methods=['GET'])
def verify_email_form():
    email = request.args.get('email')  
    return render_template('verify_eamil.html', email=email)


@auth.route('/verify_email', methods=['POST'])
def verify_email():
    try:
        email = request.form['email']
        verification_code = request.form['verification_code']

        cursor = db.cursor()
        query = "SELECT * FROM email_verification WHERE email = %s AND verification_code = %s"
        cursor.execute(query, (email, verification_code))
        verification_result = cursor.fetchone()

        if verification_result:
            cursor.execute("UPDATE users SET is_verified = 1 WHERE email = %s", (email,))
            cursor.execute("DELETE FROM email_verification WHERE email = %s", (email,))
            db.commit()
            cursor.close()

            flash('Email verification successful. You can now access the onboarding dashboard.', 'success')
            return redirect(url_for('auth.registration_form'))
        else:
            flash('Email verification failed. Please check your email and code.', 'error')
            return redirect(url_for('auth.verify_email_form', email=email))
    except Exception as e:
        flash('Error: ' + str(e), 'error')
        return redirect(url_for('auth.verify_email_form', email=email))

@auth.route('/dashboard')
def dashboard():
    if 'email' in session:
        email = session['email']
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_info = cursor.fetchone()
        cursor.close()

        if user_info['is_verified']:
            if user_info['onboarding_completed']:
                return redirect(url_for('auth.product_details'))
            else:
                return redirect(url_for('auth.on_board_dashboarding'))
        else:
            flash('Email not verified. Please verify your email to access the dashboard.', 'error')
            return redirect(url_for('auth.verify_email_form'))
    else:
        flash('Login required to access the dashboard.', 'error')
        return redirect(url_for('auth.registration_form'))


@auth.route('/product', methods=['GET'])
def product_details():
    if 'email' in session:
        email = session['email']
        cursor = db.cursor()
        cursor.execute("SELECT * FROM onboarding_registration WHERE email = %s", (email,))
        user_info = cursor.fetchone()
        cursor.close()

        if user_info:
            return render_template('product_details.html', onboarding_registration=user_info)

    flash('Login required to access the dashboard.', 'error')
    return redirect(url_for('auth.registration_form'))


@auth.route('/update_product', methods=['POST'])
def update_product():
    if 'email' in session:
        email = session['email']
        item_name = request.form.get('item_name')
        new_stock_str = request.form.get('new_stock')
        new_listing_str = request.form.get('new_listing')
        discount_str = request.form.get('discount')

        # Check if new_stock and new_listing are not empty
        if new_stock_str and new_listing_str:
            new_stock = int(new_stock_str)
            new_listing = float(new_listing_str)
        else:
            return redirect(url_for('auth.product_details'))

        if discount_str:
            discount = float(discount_str)
        else:
            discount = 0

        discounted_price = new_listing - (new_listing * (discount / 100))

        cursor = db.cursor()
        cursor.execute("UPDATE onboarding_registration SET stock = %s, listing = %s WHERE item_name = %s",
                       (new_stock, discounted_price, item_name))
        db.commit()

        cursor.execute("SELECT * FROM onboarding_registration WHERE item_name = %s", (item_name,))
        updated_product = cursor.fetchone()
        cursor.close()

        # Pass the updated product information to the template
        return render_template('product_details.html', onboarding_registration=updated_product)
    else:
        flash('Login required to access the dashboard.', 'error')
        return redirect(url_for('auth.registration_form'))



@auth.route('/add_product', methods=['POST'])
def add_product():
    if 'email' in session:
        email = session['email']
        product_name = request.form.get('product_name')
        product_price_str = request.form.get('product_price')
        product_listing_str = request.form.get('product_listing')

        if product_price_str and product_listing_str:
            product_price = float(product_price_str)
            product_listing = float(product_listing_str)
        else:
            flash('Product price and listing are required.', 'error')
            return redirect(url_for('auth.product_details'))

        cursor = db.cursor()
        cursor.execute("INSERT INTO products (product_name, price, listing, email) VALUES (%s, %s, %s, %s)",
                        (product_name, product_price, product_listing, email))
        db.commit()
        cursor.close()

        # Get the updated list of products for the user
        user_products = get_user_products(email)

        # Render the same page with the updated product list
        cursor = db.cursor()
        cursor.execute("SELECT * FROM onboarding_registration WHERE email = %s", (email,))
        onboarding_registration = cursor.fetchone()
        cursor.close()

        return render_template('product_details.html', updated_product=True, onboarding_registration=onboarding_registration, user_products=user_products)
    else:
        flash('Login required to access the dashboard.', 'error')
        return redirect(url_for('auth.registration_form'))


# Add a function to retrieve user products
def get_user_products(email):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products WHERE email = %s", (email,))
    user_products = cursor.fetchall()
    cursor.close()
    return user_products
# ...









@auth.route('/admin1/',methods=['GET'])
def admin_home():
    return render_template('admin_login.html')


@auth.route('/admin_login/', methods=['POST'])
def admin_login2():
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
            return redirect(url_for('auth.admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('admin_login.html')

@auth.route('/admin_dashboard')
def admin_dashboard():
    if 'is_admin' in session:  # Check for the 'is_admin' key in session
        cursor = db.cursor()
        
        # Retrieve all vendor data
        cursor.execute("SELECT * FROM users ")
        vendors = cursor.fetchall()
        
        # Retrieve all products from vendors
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        
        cursor.close()

        return render_template('admin_dashboard.html', vendors=vendors, products=products)
    else:
        flash('Login required to access the admin dashboard.', 'error')
        return redirect(url_for('auth.admin_login'))