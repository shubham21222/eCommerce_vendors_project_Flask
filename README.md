# E-commerce Vendors Platform

The E-commerce Vendors Platform is a comprehensive web-based system designed to facilitate seamless management for vendors operating in the e-commerce domain. This platform empowers vendors to perform essential CRUD (Create, Read, Update, Delete) operations on their products, ensuring efficient and organized management of their online store. Additionally, the platform incorporates email verification features for enhanced security and user authentication.

## Table of Contents

1. [Introduction](#introduction)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [Database Initialization and Configuration](#database-initialization-and-configuration)
7. [Running the Application](#running-the-application)
8. [Functionalities](#functionalities)
9. [Email Verification](#email-verification)
10. [Contributing](#contributing)


## Introduction

The E-commerce Vendors Platform provides a user-friendly interface for vendors to manage their product listings effectively. Vendors can perform CRUD operations on the platform, allowing them to add new products, update existing ones, view product details, and remove products as needed. The incorporation of email verification ensures secure access and authentication for vendors.

## Technology Stack

### Frontend

- HTML
- CSS
- JavaScript

### Backend

- Python
- Flask (Web Framework)
- pymysql (Database ORM)
- WTForms (Form Handling)
- Flask-Mail (Email Sending)

## Project Structure

The project directory comprises the following key components:

- `app.py`: The main application file that initializes the Flask instance and connects various functionalities.
- `models.py`: Defines the database models using SQLAlchemy.
- `forms.py`: Manages web forms using WTForms for user input validation.
- `views.py`: Contains views for handling CRUD operations and rendering templates.
- `utils.py`: Utility functions for various tasks, including email verification.
- `templates/`: Directory containing HTML templates.
- `static/`: Directory for static assets such as CSS and images.

## Prerequisites

Before proceeding, ensure that the following dependencies are installed on your system:

- Python 3.x
- Git
- Flask
- pyMYsql
- WTForms
- Flask-Mail

## Installation

1. Clone the GitHub repository to your desired location:

   ```bash
      git clone https://github.com/yourusername/ecommerce-vendors-platform.git
   ```

2. Navigate to the "CMS" directory:

   ```bash
   cd ecommerce-vendors-platform

   ```

3. Install the required packages and libraries by executing:

   ```bash
   pip install -r requirements.txt
   ```

## Database Initialization and Configuration

1. Before running the application, initialize the database by executing the following commands:

```bash
flask db init
flask db migrate
flask db upgrade
```



2. Update the MySQL database configuration in the `db.py` file. Open `db.py` and provide your MySQL database connection details as follows:

   ```python
   db_config = {
       "host": "your_database_host",
       "user": "your_database_user",
       "password": "your_database_password",
       "database": "your_database_name"
   }
   ```

   Save the changes.

## Running the Application

To launch the application, execute the following command:

```bash
flask --app app.py run
```

This command will start the Flask development server, and you can access the Application in your web browser at http://localhost:5000.

## Functionalities

1.The E-commerce Vendors Platform provides the following essential functionalities:

2.Vendor Registration and Authentication: Vendors can register with a valid email, and user authentication is enforced.

3.Product CRUD Operations: Vendors can create, view, update, and delete their products.

4.Responsive Design: The platform is designed to work seamlessly on various devices.


## Email Verification
The platform incorporates email verification to enhance security. Upon registration, vendors receive an email with a verification link. Clicking the link verifies their email address and activates their account.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.
