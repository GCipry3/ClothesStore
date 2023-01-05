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
            CHECK ( LENGTH(billing_address) >= 5 ),
            CHECK ( email REGEXP '[a-z0-9._%-]+@[a-z0-9._%-]+\.[a-z]{2,4}' ),
            CHECK ( LENGTH(name) >= 2 AND name REGEXP '^[a-zA-Z ]*$' ),
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
            quantity INT NOT NULL DEFAULT 1,
            CHECK ( LENGTH(description) >= 5),
            CHECK ( quantity > 0 ),
            CHECK ( LENGTH(name) >= 2 ),
            CHECK (price > 0)
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
            CHECK ( LENGTH(shipping_address) >= 5 ),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    ''')

    #order_items table
    cursor.execute('''
        CREATE TABLE order_items (
            order_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL,
            CHECK ( quantity > 0 ),
            PRIMARY KEY (order_id, product_id),
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    ''')
    cursor.execute("COMMIT")


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
    cursor.execute("COMMIT")


def insert_data():
    conn = connect_to_database()
    cursor = conn.cursor()

    #customers
    cursor.execute('''
        INSERT INTO customers (name, email, billing_address) VALUES 
            ('Galbeaza Ciprian', 'galbeazaciprian@gmail.com', 'Iasi, Aleea Pacurari , nr 10'), 
            ('Acatrinei Andra', 'acatrineiandra@gmail.com', 'Iasi, Strada Bistrita, nr 8'), 
            ('Diaconu Mara', 'diaconumara12@gmail.com', 'Timisoara, Strada Mihai Eminescu, nr 10'),
            ('Popa Ion', 'popaion512@gmail.com', 'Bucuresti, Strada Ion Creanga, nr 21'),
            ('Zaharia Alexandru', 'alexandruzaharia@gmail.com', 'Cluj-Napoca, Strada Alexandru Vaida Voievod, nr 11'),
            ('Florea Cosmin', 'floreacosmin11@gmail.com', 'Bucuresti, Strada Ion Creanga, nr 2'),
            ('Dimitrescu Ioana', 'dimitrescuioana4@gmail.com', 'Brasov, Aleea Lupeni, nr 13'),
            ('Artene Raluca', 'arteneraluca0@gmail.com', 'Brasov, Strada Izvorului, nr 5'),
            ('Simion Tiberius', 'simiontiberius@gmail.com', 'Constanta, Strada 23 August, nr 1'),
            ('Marinescu Andreea', 'marinescuandreea9@gmail.com', 'Constanta, Strada Calatis, nr 8'),
            ('Iorga Florin', 'iorgaflorin@gmail.com', 'Oradea, Strada Luptei, nr 7'),
            ('Anton Adrian', 'adriananton67@gmail.com', 'Oradea, Strada Transilvaniei, nr 30')
    ''')

    #products
    cursor.execute('''
        INSERT INTO products (name, quantity,price, description) VALUES
            ('T-Shirt',70, 29, 'Short sleeve t-shirt'),
            ('Dress',40, 79, 'Short sleeve dress'),
            ('Jeans',60, 59, 'Blue jeans'),
            ('Shorts',40, 39, 'Denim shorts'),
            ('Skirt',30, 49, 'Midi length skirt'),
            ('Blouse',70, 69, 'White blouse'),
            ('Shirt',80, 59, 'Button-up shirt'),
            ('Sweater',100, 79, 'Crew neck sweater'),
            ('Coat',30, 99, 'Trench coat'),
            ('Jacket',30, 79, 'Leather jacket'),
            ('Hoodies',50, 89, 'Polyester Hoodie'),
            ('Sleepwear',40, 39, 'Cotton sleepwear')
    ''')

    #categories
    cursor.execute('''
        INSERT INTO categories (name) VALUES
            ('T-Shirts'),
            ('Dresses'),
            ('Jeans'),
            ('Shorts'),
            ('Coats'),
            ('Jackets'),
	        ('Sleepwear')
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
            (10,6),
            (11,1),
            (12,7)
    ''')

    #orders
    cursor.execute('''
       INSERT INTO orders (customer_id, order_date, shipping_address) VALUES 
	    (1, '2022-01-01', 'Iasi, Strada Bistrita, nr 8'),
	    (2, '2022-01-02', 'Iasi, Aleea Pacurari, nr 10'), 
	    (3, '2022-01-03', 'Timisoara, Strada Mihai Eminescu, nr 10'),
	    (4, '2022-01-04', 'Bucuresti, Strada Ion Creanga, nr 21'),
	    (5, '2022-01-05', 'Cluj-Napoca, Strada Alexandru Vaida Voievod, nr 11'),
	    (6, '2022-01-06', 'Bucuresti, Strada Ion Creanga, nr 2'),
	    (7, '2022-01-07', 'Brasov, Aleea Lupeni, nr 13'),
	    (8, '2022-01-08', 'Brasov, Strada Izvorului, nr 5'),
	    (9, '2022-01-09', 'Constanta, Strada 23 August, nr 1'),
	    (10, '2022-01-10', 'Constanta, Strada Calatis, nr 8'),
	    (11, '2022-01-11', 'Oradea, Strada Luptei, nr 7'),
	    (12, '2022-01-12', 'Oradea, Strada Transilvaniei, nr 30')
    ''')

    cursor.execute("COMMIT")


def add_order_items(order_id, product_id, quantity):
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute("""
        BEGIN
    """)

    cursor.execute(f"""
        INSERT INTO order_items (order_id, product_id, quantity)
            SELECT {order_id}, {product_id}, {quantity}
            FROM dual
            WHERE {quantity} <= (SELECT quantity FROM products WHERE product_id = {product_id})
    """)

    cursor.execute(f"""
        UPDATE products
            JOIN order_items ON order_items.product_id = products.product_id
            SET products.quantity = products.quantity - order_items.quantity
            WHERE products.product_id = {product_id} AND order_items.order_id = {order_id} AND order_items.product_id = {product_id} and
                products.quantity >= order_items.quantity
    """)
    
    cursor.execute("COMMIT")


def delete_order_items(order_id, product_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT quantity FROM order_items WHERE product_id = {product_id} and order_id = {order_id}")
    quantity = cursor.fetchone()[0]

    cursor.execute(f"SELECT quantity FROM products WHERE product_id = {product_id}")
    product_quantity = cursor.fetchone()[0]

    cursor.execute(f"UPDATE products SET quantity = {product_quantity + quantity} WHERE product_id = {product_id}")
    cursor.execute(f"DELETE FROM order_items WHERE product_id = {product_id} and order_id = {order_id}")
    
    cursor.execute("COMMIT")



def delete_order(order_id):
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute(f"SELECT product_id FROM order_items WHERE order_id = {order_id}")
    products = cursor.fetchall()

    for product in products:
        product_id = product[0]
        delete_order_items(order_id, product_id)

    cursor.execute(f"DELETE FROM orders WHERE order_id = {order_id}")
    
    cursor.execute("COMMIT")