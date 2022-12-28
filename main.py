from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

DB_USER = 'root'
DB_PASSWORD = '123456789'
DB_NAME = 'storeproject'

def connect_to_database():
    conn = mysql.connector.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return conn


def create_tables():
    conn = connect_to_database()
    cursor = conn.cursor()
    
    #customers table
    cursor.execute('''
        CREATE TABLE customers (
            customer_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            billing_address VARCHAR(255) NOT NULL
        )
    ''')

    #products table
    cursor.execute('''
        CREATE TABLE products (
            product_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            description TEXT NOT NULL
        )
    ''')

    #categories table
    cursor.execute('''
        CREATE TABLE categories (
            category_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL
        )
    ''')

    #product_categories table
    cursor.execute('''
        CREATE TABLE product_categories (
            product_id INT NOT NULL,
            category_id INT NOT NULL,
            PRIMARY KEY (product_id, category_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    ''')

    #orders table
    cursor.execute('''
        CREATE TABLE orders (
            order_id INT PRIMARY KEY AUTO_INCREMENT,
            customer_id INT NOT NULL,
            order_date DATETIME NOT NULL,
            shipping_address VARCHAR(255) NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    ''')

    #order_items table
    cursor.execute('''
        CREATE TABLE order_items (
            order_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL,
            PRIMARY KEY (order_id, product_id),
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    ''')
    conn.commit()

def delete_tables():
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    conn.commit()


def insert_data():
    conn = connect_to_database()
    cursor = conn.cursor()

    #customers
    cursor.execute('''
        INSERT INTO customers (name, email, billing_address)
        VALUES
            ('Customer 1', 'customer1@example.com', 'Address 1'),
            ('Customer 2', 'customer2@example.com', 'Address 2'),
            ('Customer 3', 'customer3@example.com', 'Address 3'),
            ('Customer 4', 'customer4@example.com', 'Address 4'),
            ('Customer 5', 'customer5@example.com', 'Address 5'),
            ('Customer 6', 'customer6@example.com', 'Address 6'),
            ('Customer 7', 'customer7@example.com', 'Address 7'),
            ('Customer 8', 'customer8@example.com', 'Address 8'),
            ('Customer 9', 'customer9@example.com', 'Address 9'),
            ('Customer 10', 'customer10@example.com', 'Address 10')
    ''')
    #products
    cursor.execute('''
        INSERT INTO products (name, price, description)
        VALUES
            ('Product 1', 10.00, 'Description 1'),
            ('Product 2', 20.00, 'Description 2'),
            ('Product 3', 30.00, 'Description 3'),
            ('Product 4', 40.00, 'Description 4'),
            ('Product 5', 50.00, 'Description 5'),
            ('Product 6', 60.00, 'Description 6'),
            ('Product 7', 70.00, 'Description 7'),
            ('Product 8', 80.00, 'Description 8'),
            ('Product 9', 90.00, 'Description 9'),
            ('Product 10', 100.00, 'Description 10')
    ''')

    #categories
    cursor.execute('''
        INSERT INTO categories (name)
        VALUES
            ('Category 1'),
            ('Category 2'),
            ('Category 3'),
            ('Category 4'),
            ('Category 5'),
            ('Category 6'),
            ('Category 7'),
            ('Category 8'),
            ('Category 9'),
            ('Category 10')
    ''')

    #product_categories
    cursor.execute('''
        INSERT INTO product_categories (product_id, category_id)
        VALUES
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (8, 8),
            (9, 9),
            (10, 10)
    ''')

    #orders
    cursor.execute('''
        INSERT INTO orders (customer_id, order_date, shipping_address)
        VALUES
            (1, '2020-01-01 00:00:00', 'Address 1'),
            (2, '2020-01-02 00:00:00', 'Address 2'),
            (3, '2020-01-03 00:00:00', 'Address 3'),
            (4, '2020-01-04 00:00:00', 'Address 4'),
            (5, '2020-01-05 00:00:00', 'Address 5'),
            (6, '2020-01-06 00:00:00', 'Address 6'),
            (7, '2020-01-07 00:00:00', 'Address 7'),
            (8, '2020-01-08 00:00:00', 'Address 8'),
            (9, '2020-01-09 00:00:00', 'Address 9'),
            (10, '2020-01-10 00:00:00', 'Address 10')
    ''')

    #order_items
    cursor.execute('''
        INSERT INTO order_items (order_id, product_id, quantity)
        VALUES
            (1, 1, 1),
            (2, 2, 2),
            (3, 3, 3),
            (4, 4, 4),
            (5, 5, 5),
            (6, 6, 6),
            (7, 7, 7),
            (8, 8, 8),
            (9, 9, 9),
            (10, 10, 10)
    ''')

    conn.commit()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/create-tables',methods=['POST'])
def handle_create_tables():
    create_tables()
    return 'Tables created'

@app.route('/insert-data',methods=['POST'])
def handle_insert_data():
    insert_data()
    return 'Data inserted'

@app.route('/delete-tables',methods=['POST'])
def handle_delete_tables():
    delete_tables()
    return 'Tables deleted'

@app.route('/get-customers')
def handle_get_customers():
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()

    return render_template('customers.html', customers=customers)