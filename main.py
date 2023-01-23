<<<<<<< HEAD
from flask import Flask, render_template, request, redirect
from database_management import *
=======
from flask import Flask, request, render_template
import mysql.connector

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

    # Create the Customers table
    query = """
        CREATE TABLE Customers (
            customer_id INTEGER PRIMARY KEY AUTO_INCREMENT,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            phone VARCHAR(255) NOT NULL,
            address VARCHAR(255) NOT NULL
        )
    """
    cursor.execute(query)

    # Create the Stores table
    query = """
        CREATE TABLE Stores (
            store_id INTEGER PRIMARY KEY AUTO_INCREMENT,
            store_name VARCHAR(255) NOT NULL,
            address VARCHAR(255) NOT NULL,
            phone VARCHAR(255) NOT NULL
        )
    """
    cursor.execute(query)

    # Create the Items table
    query = """
        CREATE TABLE Items (
            item_id INTEGER PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            sizes VARCHAR(255) NOT NULL,
            quantity INTEGER NOT NULL
        )
    """
    cursor.execute(query)

    # Create the Orders table
    query = """
        CREATE TABLE Orders (
            order_id INTEGER PRIMARY KEY AUTO_INCREMENT,
            customer_id INTEGER NOT NULL,
            order_date DATE NOT NULL,
            total_cost DECIMAL(10,2) NOT NULL,
            store_id INTEGER NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
            FOREIGN KEY (store_id) REFERENCES Stores(store_id)
        )
    """
    cursor.execute(query)

    # Create the OrderItems table
    query = """
        CREATE TABLE OrderItems (
            order_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            PRIMARY KEY (order_id, item_id),
            FOREIGN KEY (order_id) REFERENCES Orders(order_id),
            FOREIGN KEY (item_id) REFERENCES Items(item_id)
        )
    """
    cursor.execute(query)



def delete_tables():
    conn = connect_to_database()
    cursor = conn.cursor()

    # Disable foreign key checks to allow the tables to be deleted
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

    # Retrieve the names of all tables in the database
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    # Iterate through the list of table names and delete each table
    for table in tables:
        table_name = table[0]
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        
    # Re-enable foreign key checks
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")



# Get function that returns all the rows from a table
def get_everything_from_table(table_name):
    conn = connect_to_database()
    cursor = conn.cursor()

    # Query the database for a list of items
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    items = cursor.fetchall()

    return items

>>>>>>> 8279490 (update)

app = Flask(__name__)

@app.route('/')
<<<<<<< HEAD
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/create-tables',methods=['POST'])
def handle_create_tables():
    try:
        create_tables()
    except Exception as e:
        return render_template('home.html',text='Tables already exist')
    
    return render_template('home.html',text='Tables created')


@app.route('/insert-data',methods=['POST'])
def handle_insert_data():
    try:
        insert_data()
    except Exception as e:
        return render_template('home.html',text=f'Tables do not exist or Data already inserted ! Exception :{e}')
    
    return render_template('home.html',text='Data inserted')


@app.route('/delete-data',methods=['POST'])
def handle_delete_data():
    delete_tables()
    create_tables()
    
    return render_template('home.html',text='Data deleted')


@app.route('/delete-tables',methods=['POST'])
def handle_delete_tables():
    delete_tables()
    return render_template('home.html',text='Tables deleted')


@app.route('/customers')
def handle_get_customers():
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM customers")
        customers = cursor.fetchall()
    except Exception as e:
        return render_template('customers.html')
    return render_template('customers.html', customers=customers)


@app.route('/add-customer', methods=['POST'])
def handle_add_customer():
    name = request.form['name']
    email = request.form['email']
    billing_address = request.form['billing_address']

    conn = connect_to_database()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO customers (name, email, billing_address) VALUES (%s, %s, %s)", (name, email, billing_address))
    except Exception as e:
        return render_template ('home.html',text=f'Invalid Insert , Exception :{e}')

    cursor.execute("COMMIT")

    return redirect('/customers')


@app.route('/remove-customer', methods=['POST'])
def handle_remove_customer():
    customer_id = request.form['customer_id']

    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM customers WHERE customer_id = {customer_id}")
    except Exception as e:
        return render_template ('home.html',text=f'Invalid Delete: {customer_id} , Exception :{e}')
    cursor.execute("COMMIT")

    return redirect('/customers')


@app.route('/update-customer', methods=['POST','GET'])
def handle_default_update_customer():
    customer_id = request.form['customer_id']

    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute(f"SELECT True FROM customers WHERE customer_id = {customer_id}")
    if cursor.fetchone() is None:
        return render_template ('home.html',text=f'Invalid Customer ID: {customer_id}')
    
    cursor.execute(f"SELECT * FROM customers WHERE customer_id = {customer_id}")
    customer = cursor.fetchone()

    return render_template('update_customer.html', customer=customer)
    

@app.route('/execute-update-customer', methods=['POST'])
def handle_execute_update_customer():
    customer_id = request.form['customer_id']
    name = request.form['name']
    email = request.form['email']
    billing_address = request.form['billing_address']

    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        cursor.execute(f"UPDATE customers SET name = '{name}', email = '{email}', billing_address = '{billing_address}' WHERE customer_id = {customer_id}")
    except Exception as e:
        return render_template ('home.html',text=f'Invalid Update: {customer_id} , Exception :{e}')

    cursor.execute("COMMIT")

    return redirect('/customers')



@app.route('/products')
def handle_get_products():
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT p.product_id AS id, p.name,p.price,p.description,p.quantity,
                (
                    SELECT GROUP_CONCAT(c.name SEPARATOR ',')
                    FROM categories c
                    WHERE c.category_id IN (
                        SELECT pc.category_id
                        FROM product_categories pc
                        WHERE pc.product_id = p.product_id
                    )
                ) AS categories
            FROM products p
        """)
        products_with_categories = cursor.fetchall()

        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
    except Exception as e:
        return render_template('products.html')

    return render_template('products.html', products=products_with_categories , categories=categories)

@app.route('/add-product', methods=['POST'])
def handle_add_product():
    name = request.form['name']
    price = request.form['price']
    description = request.form['description']
    quantity = request.form['quantity']

    conn = connect_to_database()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO products (name, price, description, quantity) VALUES (%s, %s, %s, %s)", (name, price, description, quantity))
        cursor.execute("COMMIT")
    except Exception as e:
        return render_template ('home.html',text=f'Invalid Insert , Exception :{e}')

    return redirect('/products')


@app.route('/remove-product', methods=['POST'])
def handle_remove_product():
    product_id = request.form['product_id']

    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM product_categories WHERE product_id = {product_id}")
    cursor.execute(f"DELETE FROM products WHERE product_id = {product_id}")

    cursor.execute("COMMIT")

    return redirect('/products')


@app.route('/update-product', methods=['POST','GET'])
def handle_default_update_product():
    product_id = request.form['product_id']

    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM products WHERE product_id = {product_id}")
    product = cursor.fetchone()

    return render_template('update_product.html', product=product)
    

@app.route('/execute-update-product', methods=['POST'])
def handle_execute_update_product():
    product_id = request.form['product_id']
    name = request.form['name']
    price = request.form['price']
    description = request.form['description']

    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute(f"UPDATE products SET name = '{name}', price = '{price}', description = '{description}' WHERE product_id = {product_id}")
        cursor.execute("COMMIT")
    except Exception as e:
        return render_template ('home.html',text=f'Invalid Update: {product_id} , Exception :{e}')
    
    return redirect('/products') 

@app.route('/add-category', methods=['POST'])
def handle_add_category():
    name = request.form['name']

    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO categories (name) VALUES ('{name}')")
    cursor.execute("COMMIT")

    return redirect('/products')


@app.route('/remove-category', methods=['POST'])
def handle_remove_category():
    category_id = request.form['category_id']

    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM product_categories WHERE category_id = {category_id}")
    cursor.execute(f"DELETE FROM categories WHERE category_id = {category_id}")

    cursor.execute("COMMIT")

    return redirect('/products')


@app.route('/add-product-category', methods=['POST'])
def handle_add_product_category():
    product_id = request.form['product_id']
    category_id = request.form['category_id']

    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO product_categories (product_id, category_id) VALUES ({product_id}, {category_id})")
        cursor.execute("COMMIT")
    except Exception as e:
        return render_template ('home.html',text=f'Invalid Insert , Exception :{e}')
        
    return redirect('/products')

@app.route('/orders', methods=['GET'])
def handle_get_orders():
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT o.order_id, o.customer_id, o.order_date, o.shipping_address, SUM(oi.quantity * p.price)
            FROM orders o
            LEFT JOIN order_items oi ON o.order_id = oi.order_id
            LEFT JOIN products p ON oi.product_id = p.product_id
            GROUP BY o.order_id
        """)
        orders = cursor.fetchall()

    except Exception as e:
        return render_template('orders.html')

    return render_template('orders.html', orders=orders )

@app.route('/add-order', methods=['POST'])
def handle_add_order():
    customer_id = request.form['customer_id']
    order_date = request.form['order_date']
    shipping_address = request.form['shipping_address']

    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO orders (customer_id, order_date, shipping_address) VALUES (%s, %s, %s)", (customer_id, order_date, shipping_address))
        cursor.execute("COMMIT")
    except Exception as e:
        return render_template ('home.html',text=f'Invalid Insert , Exception :{e}')
    

    return redirect('/orders')


@app.route('/open-basket', methods=['POST'])
def handle_add_order_items():
    order_id = request.form['order_id']
=======
def home():
    return render_template('home.html')

@app.route('/create-tables', methods=['POST'])
def handle_create_tables():
    create_tables()
    return 'Tables created successfully!'


@app.route('/delete-tables', methods=['POST'])
def handle_delete_tables():
    delete_tables()
    return 'Tables deleted successfully!'

@app.route('/items')
def items():
    # Query the database for a list of items
    items = get_everything_from_table("items")
    return render_template('items.html', items=items)

@app.route('/customers')
def customers():
    # Query the database for a list of customers
    customers = get_everything_from_table("customers")
    return render_template('customers.html', customers=customers)

@app.route('/orders')
def orders():
    # Query the database for a list of orders
    orders = get_everything_from_table("orders")
    return render_template('orders.html', orders=orders)

@app.route('/stores')
def stores():
    # Query the database for a list of stores
    stores = get_everything_from_table("stores")
    return render_template('stores.html', stores=stores)



@app.route('/add-order', methods=['POST'])
def add_order():
    # Get the customer ID and total cost from the form
    customer_id = request.form['customer_id']
    total_cost = request.form['total_cost']
    store_id = request.form['store_id']
>>>>>>> 8279490 (update)

    conn = connect_to_database()
    cursor = conn.cursor()

<<<<<<< HEAD
    cursor.execute(f"SELECT 'True' FROM orders WHERE order_id = {order_id}")
    if cursor.fetchone() is None:
        return render_template('home.html', text = "Order does not exist")

    cursor.execute(f"SELECT o.order_id,o.product_id,o.quantity,p.name FROM order_items o,products p WHERE o.order_id = {order_id} AND o.product_id = p.product_id")
    order_items = cursor.fetchall()

    cursor.execute(f"SELECT * FROM products")
    products = [list(t) for t in cursor.fetchall()]

    """for order_item in order_items:
        order_item = list(order_item)
        cursor.execute(f"SELECT name FROM products WHERE product_id = {order_item[1]}")
        order_item.append(cursor.fetchone()[0])"""
    
    cursor.execute(f"SELECT SUM(p.price * o.quantity) FROM order_items o, products p WHERE o.order_id = {order_id} AND o.product_id = p.product_id")
    total = cursor.fetchone()[0]

    return render_template('basket.html', order_items=order_items, products=products, order_id=order_id,total=total)


@app.route('/execute-add-order-items', methods=['POST'])
def handle_execute_add_order_items():
    order_id = request.form['order_id']
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
=======
    # Insert a new order into the orders table
    query = "INSERT INTO orders (customer_id, order_date,total_cost,store_id) VALUES (%s, CURDATE(),%s,%s)"
    values = (customer_id, total_cost,store_id)
    cursor.execute(query, values)
    conn.commit()

    return 'Order added successfully!'

@app.route('/add-item', methods=['POST'])
def add_item():
    # Get the name, price, description, and category from the form
    name = request.form['name']
    price = request.form['price']
    description = request.form['description']
    category = request.form['category']
>>>>>>> 8279490 (update)

    conn = connect_to_database()
    cursor = conn.cursor()

<<<<<<< HEAD
    cursor.execute(f"""
        SELECT quantity FROM products WHERE product_id = {product_id}
    """)
    product_quantity = cursor.fetchone()

    if product_quantity is None:
        return render_template('home.html', text = f"Product '{product_id}' does not exist")
    else:
        product_quantity = product_quantity[0]


    try:
        if not add_order_items(order_id=order_id, product_id=product_id, quantity=quantity):
            return render_template('home.html', text = f"Not enought quantity for product '{product_id}', asked quantity: '{quantity}' , available quantity: {product_quantity}")
    except Exception as e:
        return render_template('home.html', text = f"Invalid Insert , Exception :{e}")
    return redirect('/orders')


@app.route('/remove-order-item', methods=['POST'])
def handle_remove_order_item():
    product_id = request.form['product_id']
    order_id = request.form['order_id']

    if not delete_order_items(order_id=order_id, product_id=product_id):
        return render_template('home.html', text = f"Product '{product_id}' does not exist in order '{order_id}'")

    return redirect('/orders')


@app.route('/update-order-item', methods=['POST'])
def handle_update_order_item():
    product_id = request.form['product_id']
    order_id = request.form['order_id']
    quantity = request.form['quantity']
    
    if not delete_order_items(order_id=order_id, product_id=product_id) or\
        not add_order_items(order_id=order_id, product_id=product_id, quantity=quantity):
        return render_template('home.html', text = f"Product '{product_id}' does not exist in order '{order_id}'")
    
    return redirect('/orders')

@app.route('/remove-order', methods=['POST'])
def handle_remove_order():
    order_id = request.form['order_id']
=======
    # Insert a new item into the items table
    query = "INSERT INTO items (name, price, description, category) VALUES (%s, %s, %s, %s)"
    values = (name, price, description, category)
    cursor.execute(query, values)
    conn.commit()

    return 'Item added successfully!'

@app.route('/add-customer', methods=['POST'])
def add_customer():
    # Get the name, email, and phone from the form
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
>>>>>>> 8279490 (update)

    conn = connect_to_database()
    cursor = conn.cursor()

<<<<<<< HEAD
    delete_order(order_id=order_id)

    return redirect('/orders')


@app.route('/add-product-quantity', methods=['POST'])
def handle_add_product_quantity():
    product_id = request.form['product_id']
    quantity = request.form['quantity']

    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute(f"UPDATE products SET quantity = quantity + {quantity} WHERE product_id = {product_id}")
        cursor.execute("COMMIT")
    except Exception as e:
        return render_template ('home.html',text=f'Invalid Insert , Exception :{e}')
    return redirect('/products')
=======
    # Insert a new customer into the customers table
    query = "INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)"
    values = (name, email, phone)
    cursor.execute(query, values)
    conn.commit()

    return 'Customer added successfully!'
>>>>>>> 8279490 (update)
