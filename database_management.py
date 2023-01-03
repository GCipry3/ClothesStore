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
            billing_address VARCHAR(255) NOT NULL,
            constraint unique_email UNIQUE (email)
        )
    ''')

    #products table
    cursor.execute('''
        CREATE TABLE products (
            product_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            description TEXT NOT NULL,
            quantity INT NOT NULL,
            constraint positive_price check (price > 0)
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
        INSERT INTO customers (name, email, billing_address) VALUES 
            ('John Smith', 'john@example.com', 'Iasi, Aleea Pacurari, nr 10'), 
            ('Jane Doe', 'jane@example.com', 'Iasi, Miroslava, Strada Florilor , nr 25'), 
            ('Bob Johnson', 'bob@example.com', 'Timisoara, Strada Mihai Eminescu, nr 10'),
            ('Samantha Williams', 'samantha@example.com', 'Bucuresti, Strada Ion Creanga, nr 21'),
            ('Emily Thompson', 'emily@example.com', 'Cluj-Napoca, Strada Alexandru Vaida Voievod, nr 11'),
            ('Kimberly Kim', 'kimberly@example.com', 'Bucuresti, Strada Ion Creanga, nr 2')
    ''')

    #products
    cursor.execute('''
        INSERT INTO products (name, quantity,price, description) VALUES
            ('T-Shirt',30, 29, 'Short sleeve t-shirt'),
            ('Dress',30, 79, 'Short sleeve dress'),
            ('Jeans',30, 59, 'Blue jeans'),
            ('Shorts',30, 39, 'Denim shorts'),
            ('Skirt',30, 49, 'Midi length skirt'),
            ('Blouse',30, 69, 'White blouse'),
            ('Shirt',30, 59, 'Button-up shirt'),
            ('Sweater',30, 79, 'Crew neck sweater'),
            ('Coat',30, 99, 'Trench coat'),
            ('Jacket',30, 79, 'Leather jacket')
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
        INSERT INTO product_categories (product_id, category_id) VALUES
            (1,1),
            (2,2),
            (3,3),
            (4,4),
            (5,2),
            (6,2),
            (7,1),
            (8,1),
            (9,5),
            (9,6),
            (10,6)
    ''')

    #orders
    cursor.execute('''
        INSERT INTO orders (customer_id, order_date, shipping_address) VALUES 
            (1, '2022-01-01 12:00:00', 'Iasi , Aleeaa Pacurari, nr 10'),
            (2, '2022-01-02 13:00:00', 'Iasi, Miroslava, Strada Florilor , nr 25'),
            (2, '2022-01-03 14:00:00', 'Timisoara, Strada Mihai Eminescu, nr 10'),
            (4, '2022-01-04 15:00:00', 'Bucuresti, Strada Vasile Alecsandri, nr 25'),
            (5, '2022-01-05 16:00:00', 'Cluj-Napoca, Strada Alexandru Vaida Voievod, nr 11'),
            (6, '2022-01-06 17:00:00', 'Bucuresti, Strada Ion Creanga, nr 2')
    ''')

    conn.commit()

