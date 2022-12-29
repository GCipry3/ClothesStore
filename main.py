from flask import Flask, render_template, request, redirect
from database_management import *

app = Flask(__name__)


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


@app.route('/customers')
def handle_get_customers():
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()

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
