import pymysql
import bcrypt

# MySQL database connection configuration
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DB = 'ecommarce'

# Create a connection to the database
db = pymysql.connect(
    host=MYSQL_HOST, port=MYSQL_PORT,
    user=MYSQL_USER, password=MYSQL_PASSWORD,
    db=MYSQL_DB, cursorclass=pymysql.cursors.DictCursor
)

# Admin credentials
admin_username = 'shubham2122'
admin_password = '9806265682'  # Replace with the actual admin password

# Hash the admin password
hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())

# Insert the admin credentials into the database
try:
    cursor = db.cursor()
    insert_query = "INSERT INTO admin_credentials (username, password) VALUES (%s, %s)"
    cursor.execute(insert_query, (admin_username, hashed_password))
    db.commit()
    cursor.close()
    print("Admin credentials inserted successfully.")
except Exception as e:
    db.rollback()
    print("Error:", str(e))

# Close the database connection
db.close()
