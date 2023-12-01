import pymysql

# Database configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'NewPassword123!'
DB_NAME = 'ecommarce'

# Connect to MySQL server
connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Create database
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")

# Switch to the newly created database
cursor.execute(f"USE {DB_NAME}")

# Define table creation queries
table_queries = [
    """
    CREATE TABLE IF NOT EXISTS admin_credentials (
      username varchar(255) NOT NULL,
      password varchar(255) NOT NULL,
      PRIMARY KEY (username)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS contact_form_data (
      id int NOT NULL AUTO_INCREMENT,
      full_name varchar(255) NOT NULL,
      mobile_number varchar(20) NOT NULL,
      description text NOT NULL,
      submission_date timestamp NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS contacts (
      id int NOT NULL AUTO_INCREMENT,
      username varchar(255) NOT NULL,
      password varchar(255) NOT NULL,
      PRIMARY KEY (id),
      UNIQUE KEY username (username)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS email_verification (
      id int NOT NULL AUTO_INCREMENT,
      email varchar(255) NOT NULL,
      verification_code varchar(6) NOT NULL,
      PRIMARY KEY (id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS onboarding_registration (
      email varchar(255) NOT NULL,
      item_name varchar(255) NOT NULL,
      listing varchar(255) NOT NULL,
      stock varchar(255) NOT NULL,
      pickup_address varchar(255) NOT NULL,
      pickup_pincode varchar(10) NOT NULL,
      bank_account varchar(20) NOT NULL,
      ifsc_code varchar(20) NOT NULL,
      PRIMARY KEY (email)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS products (
      product_id int NOT NULL AUTO_INCREMENT,
      product_name varchar(255) NOT NULL,
      price decimal(10,2) NOT NULL,
      listing bigint DEFAULT NULL,
      email varchar(255) NOT NULL,
      stock decimal(10,2) DEFAULT NULL,
      status varchar(20) DEFAULT 'Pending',
      PRIMARY KEY (product_id),
      KEY email (email),
      CONSTRAINT products_ibfk_1 FOREIGN KEY (email) REFERENCES onboarding_registration (email)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS users (
      username varchar(255) NOT NULL,
      password varchar(255) NOT NULL,
      first_name varchar(50) DEFAULT NULL,
      last_name varchar(50) DEFAULT NULL,
      email varchar(100) DEFAULT NULL,
      address varchar(255) DEFAULT NULL,
      city varchar(100) DEFAULT NULL,
      state varchar(255) DEFAULT NULL,
      product_detail text,
      is_verified tinyint(1) DEFAULT NULL,
      PRIMARY KEY (username)
    )
    """
]

# Execute table creation queries
for query in table_queries:
    cursor.execute(query)

# Commit changes and close the connection
connection.commit()
connection.close()
