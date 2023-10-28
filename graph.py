from flask import Blueprint, render_template, redirect, url_for, request, flash, session ,get_flashed_messages ,jsonify
import pymysql
import matplotlib.pyplot as plt


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