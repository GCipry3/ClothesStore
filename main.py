from flask import Flask, render_template, request, redirect
from database_management import *

app = Flask(__name__)

@app.route('/')
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
        return render_template('home.html',text='Tables do not exist')
    
    return render_template('home.html',text='Data inserted')


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

    cursor.execute("INSERT INTO customers (name, email, billing_address) VALUES (%s, %s, %s)", (name, email, billing_address))
    conn.commit()

    return redirect('/customers')


@app.route('/remove-customer', methods=['POST'])
def handle_remove_customer():
    customer_id = request.form['customer_id']

    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM customers WHERE customer_id = {customer_id}")
    conn.commit()

    return redirect('/customers')


@app.route('/update-customer', methods=['POST','GET'])
def handle_default_update_customer():
    customer_id = request.form['customer_id']

    conn = connect_to_database()
    cursor = conn.cursor()

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

    cursor.execute(f"UPDATE customers SET name = '{name}', email = '{email}', billing_address = '{billing_address}' WHERE customer_id = {customer_id}")
    conn.commit()

    return redirect('/customers')



@app.route('/products')
def handle_get_products():
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM products")
        products = [list(t) for t in cursor.fetchall()]

        #add categories to products
        for product in products:
            cursor.execute(f"SELECT category_id from product_categories WHERE product_id = {product[0]}")
            all_categories = cursor.fetchall()
            categories=""

            for category in all_categories:
                cursor.execute(f"SELECT name from categories WHERE category_id = {category[0]}")
                categories += "".join(cursor.fetchone()) + ", "
            
            categories = categories[:-2]

            if categories == "":
                categories = "No categories"

            product.append(categories)

    except Exception as e:
        return render_template('products.html')

    try:
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
    except Exception as e:
        return render_template('products.html', products=products)

    return render_template('products.html', products=products , categories=categories)

@app.route('/add-product', methods=['POST'])
def handle_add_product():
    name = request.form['name']
    price = request.form['price']
    description = request.form['description']

    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO products (name, price, description) VALUES (%s, %s, %s)", (name, price, description))
    conn.commit()

    return redirect('/products')


@app.route('/remove-product', methods=['POST'])
def handle_remove_product():
    product_id = request.form['product_id']

    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM products WHERE product_id = {product_id}")
    conn.commit()

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

    cursor.execute(f"UPDATE products SET name = '{name}', price = '{price}', description = '{description}' WHERE product_id = {product_id}")
    conn.commit()

    return redirect('/products') 

@app.route('/add-category', methods=['POST'])
def handle_add_category():
    name = request.form['name']

    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO categories (name) VALUES ('{name}')")
    conn.commit()

    return redirect('/products')

@app.route('/add-product-category', methods=['POST'])
def handle_add_product_category():
    product_id = request.form['product_id']
    category_id = request.form['category_id']

    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO product_categories (product_id, category_id) VALUES ({product_id}, {category_id})")
    conn.commit()

    return redirect('/products')