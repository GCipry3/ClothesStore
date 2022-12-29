import mysql.connector

DB_USER = 'root'
DB_PASSWORD = '123456789'
DB_NAME = 'storeproject'

__conn = None

def connect_to_database():
    global __conn

    if __conn is None:
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
            total_price INT NOT NULL,
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
            order_item_price INT NOT NULL,
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
        INSERT INTO customers (name, email, billing_address) VALUES 
            ('John Smith', 'john@example.com', '123 Main St'), 
            ('Jane Doe', 'jane@example.com', '456 Main St'), 
            ('Bob Johnson', 'bob@example.com', '789 Main St'),
            ('Samantha Williams', 'samantha@example.com', '321 Oak Avenue'),
            ('Emily Thompson', 'emily@example.com', '753 Pine Avenue'),
            ('Kimberly Kim', 'kimberly@example.com', '369 Birch Road')
    ''')
    #products
    cursor.execute('''
        INSERT INTO products (name, price, description) VALUES
            ('T-Shirt', 29, 'Short sleeve t-shirt'),
            ('Dress', 79, 'Short sleeve dress'),
            ('Jeans', 59, 'Blue jeans'),
            ('Shorts', 39, 'Denim shorts'),
            ('Skirt', 49, 'Midi length skirt'),
            ('Blouse', 69, 'White blouse'),
            ('Shirt', 59, 'Button-up shirt'),
            ('Sweater', 79, 'Crew neck sweater'),
            ('Coat', 99, 'Trench coat'),
            ('Jacket', 79, 'Leather jacket')
    ''')

    #categories
    cursor.execute('''
        INSERT INTO categories (name) VALUES
            ('T-Shirts'),
            ('Dresses'),
            ('Jeans'),
            ('Shorts'),
            ('Coats'),
            ('Jackets')
    ''')

    #product_categories
    cursor.execute('''
        INSERT INTO product_categories (product_id, category_id)
        VALUES
            (1, 1)
    ''')

    #orders
    cursor.execute('''
        INSERT INTO orders (customer_id, order_date, total_price, shipping_address) VALUES 
            (1, '2022-01-01 12:00:00', 100, '123 Main St'),
            (2, '2022-01-02 13:00:00', 50, '456 Main St'),
            (2, '2022-01-03 14:00:00', 75, '456 Main St'),
            (4, '2022-01-04 15:00:00', 200, '321 Main St'),
            (5, '2022-01-05 16:00:00', 125, '654 Main St'),
            (6, '2022-01-06 17:00:00', 175, '987 Main St')
    ''')

    #order_items
    cursor.execute('''
        INSERT INTO products (name, price, description) VALUES
            ('Blue T-Shirt', 20, 'This is a blue T-shirt'),
            ('Red Dress', 50, 'This is a red dress'),
            ('Black Jeans', 40, 'These are black jeans'),
            ('White Shorts', 30, 'These are white shorts'),
            ('Yellow Skirt', 25, 'This is a yellow skirt'),
            ('Purple Blouse', 35, 'This is a purple blouse'),
            ('Green Shirt', 45, 'This is a green shirt'),
            ('Orange Sweater', 55, 'This is an orange sweater'),
            ('Gray Coat', 75, 'This is a gray coat'),
            ('Brown Jacket', 65, 'This is a brown jacket')
    ''')

    conn.commit()