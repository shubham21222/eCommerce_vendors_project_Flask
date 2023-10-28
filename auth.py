from flask import Blueprint, render_template, redirect, url_for, request, flash, session ,get_flashed_messages ,jsonify
import pymysql
import bcrypt
import random
import string
from email_verification import send_verification_email
from flask_mail import Mail, Message
import matplotlib.pyplot as plt
from datetime import datetime

auth = Blueprint('auth', __name__,template_folder="templates")
app_start_time = datetime.now()

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

        # Check if the username is already taken
        username_query = "SELECT username FROM users WHERE username = %s"
        cursor.execute(username_query, (username,))
        existing_username = cursor.fetchone()

        if existing_username:
            flash('Username is already taken. Please choose a different one.', 'error')
            return render_template('register.html')

        # Check if the email is already registered
        email_query = "SELECT email FROM users WHERE email = %s"
        cursor.execute(email_query, (email))
        existing_email = cursor.fetchone()

        if existing_email:
            flash('Email is already registered. Please use a different email address.', 'error')
            return render_template('register.html')

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


# Add a function to retrieve user products with a JOIN
# Modify your function to retrieve user products with a JOIN
def get_user_products_with_join(email):
    cursor = db.cursor()
    query = """
    SELECT p.product_id, p.product_name, p.price, o.item_name, p.stock, p.listing, u.username ,p.status
    FROM products p
    JOIN onboarding_registration o ON p.email = o.email
    JOIN users u ON p.email = u.email
    WHERE p.email = %s
    """
    cursor.execute(query, (email,))
    user_products = cursor.fetchall()
    cursor.close()
    return user_products




@auth.route('/product', methods=['GET'])
def product_details():
    if 'email' in session:
        email = session['email']
        user_products = get_user_products_with_join(email)  # Call the new function
        cursor = db.cursor()
        cursor.execute("SELECT * FROM onboarding_registration WHERE email = %s", (email,))
        user_info = cursor.fetchone()
        cursor.close()

        if user_info:
            return render_template('product_details2.html', onboarding_registration=user_info, user_products=user_products)  # Pass user_products to the template

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
        return render_template('product_details2.html', onboarding_registration=updated_product)
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
        product_stock_str = request.form.get('product_stock') 
        
        # Check if all required fields are provided
        if product_price_str and product_listing_str and product_stock_str:
            product_price = float(product_price_str)
            product_listing = float(product_listing_str)
            product_stock = int(product_stock_str)  # Parse product stock as an integer
        else:
            flash('Product name, price, listing, and stock are required.', 'error')
            return redirect(url_for('auth.product_details'))

        cursor = db.cursor()
        cursor.execute("INSERT INTO products (product_name, price, listing, email, stock) VALUES (%s, %s, %s, %s, %s)",  
                        (product_name, product_price, product_listing, email, product_stock))
        db.commit()
        cursor.close()

        # Get the updated list of products for the user with a JOIN
        user_products = get_user_products_with_join(email)

        # Render the same page with the updated product list
        cursor = db.cursor()
        cursor.execute("SELECT * FROM onboarding_registration WHERE email = %s", (email,))
        onboarding_registration = cursor.fetchone()
        cursor.close()

        return render_template('product_details2.html', updated_product=True, onboarding_registration=onboarding_registration, user_products=user_products)
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

from flask import request

@auth.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    uptime = datetime.now() - app_start_time

    if 'is_admin' in session:
        cursor = db.cursor()

        if request.method == 'POST':
            # Check if a vendor should be deleted
            if 'delete_vendor' in request.form:
                email = request.form['delete_vendor']
                # Perform the deletion of the vendor based on their email
                cursor.execute("DELETE FROM users WHERE email = %s", (email,))
                db.commit()
                flash(f'Vendor with email {email} has been deleted.', 'success')

            # Check if a product should be deleted
            if 'delete_product' in request.form:
                product_id = request.form['delete_product']
                # Perform the deletion of the product based on its product_id
                cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
                db.commit()
                flash(f'Product with ID {product_id} has been deleted.', 'success')

        # Retrieve all vendor data
        cursor.execute("SELECT * FROM users")
        vendors = cursor.fetchall()

        # Retrieve all products from vendors
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        # Calculate total stock and total price from products
        total_stock = sum(product['stock'] for product in products)
        total_price = sum(product['price'] for product in products)
        total_vendors = len(vendors)
        # Prepare data for the graph
        product_names = [product['product_name'] for product in products]
        product_prices = [product['price'] for product in products]

        cursor.close()

        return render_template('admin_dashboard2.html', vendors=vendors, products=products, total_stock=total_stock, total_price=total_price, product_names=product_names, product_prices=product_prices,uptime=uptime,total_vendors=total_vendors)
    else:
        flash('Login required to access the admin dashboard.', 'error')
        return redirect(url_for('auth.admin_login2'))



    

@auth.route('/edit_product', methods=['GET', 'POST'])
def edit_product():
    if 'email' in session:
        if request.method == 'GET':
            product_id = request.args.get('product_id')

            # Retrieve the product details from the database
            cursor = db.cursor()
            cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
            product = cursor.fetchone()
            cursor.close()

            if product:
                return render_template('edit_product.html', product=product, product_id=product_id)
            else:
                flash('Product not found or you do not have permission to edit it.', 'error')
                return redirect(url_for('auth.product_details'))

        if request.method == 'POST':
            product_id = request.form.get('product_id')
            new_product_name = request.form.get('product_name')
            new_price = float(request.form.get('new_price'))
            new_listing = float(request.form.get('new_listing'))
            new_stock = float(request.form.get('new_stock'))

            # Update the product details in the database
            cursor = db.cursor()
            cursor.execute("UPDATE products SET product_name = %s, price = %s, listing = %s, stock = %s WHERE product_id = %s",
                           (new_product_name, new_price, new_listing, new_stock, product_id))
            db.commit()
            cursor.close()

            flash('Product details updated successfully.', 'success')
            return redirect(url_for('auth.product_details'))
    else:
        flash('Login required to access the dashboard.', 'error')
        return redirect(url_for('auth.registration_form'))


def generate_stock_price_chart():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()

    product_names = [product['product_name'] for product in products]
    total_stock = [product['stock'] for product in products]
    total_price = [product['price'] for product in products]

    # Create a simple bar chart using Matplotlib
    plt.figure(figsize=(10, 5))
    plt.bar(product_names, total_stock, label='Stock')
    plt.bar(product_names, total_price, label='Price')
    plt.xlabel('Products')
    plt.ylabel('Values')
    plt.title('Stock and Price Data')
    plt.legend()
    
    # Save the graph as an image
    chart_image_path = 'static/graph.png'
    plt.savefig(chart_image_path)

    return chart_image_path

@auth.route('/get_stock_price_data')
def get_stock_price_data():
    chart_data = generate_stock_price_chart_data()

    return chart_data


# Generate data for the bar chart
def generate_stock_price_chart_data():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()

    labels = []  # Labels for the x-axis
    series = [[]]  # Data for the y-axis

    for product in products:
        labels.append(product['product_name'])
        series[0].push(product['stock'])  # Assuming 'stock' is the value for the y-axis

    # Construct a dictionary with the data
    chart_data = {
        labels: labels,
        series: series
    }

    return jsonify(chart_data)



@auth.route('/delete_products', methods=['POST'])
def delete_products():
    selected_product_ids = request.form.getlist('selected_products')

    if selected_product_ids:
        cursor = db.cursor()
        try:
            for product_id in selected_product_ids:
                cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
                # You can add the status update logic here as well
                new_status = 'Deleted'
                cursor.execute("UPDATE products SET status = %s WHERE product_id = %s", (new_status, product_id))

            db.commit()
        except Exception as e:
            # Handle the database deletion error
            return render_template('error.html', error_message=str(e))
        finally:
            cursor.close()

    # Retrieve product data from your database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()

    return redirect(url_for('auth.product_details'))


@auth.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        product_id = request.form['product_id']
        new_status = request.form['new_status']

        # Update the status in your database
        cursor = db.cursor()
        cursor.execute("UPDATE products SET status = %s WHERE product_id = %s", (new_status, product_id))
        db.commit()
        cursor.close()

    # Retrieve product data from your database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()

    return render_template('product_details2.html', products=products)
