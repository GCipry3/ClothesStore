# ClothesStore

This project is a __web-based__ clothing store application that allows users to create an account, 
browse and add products to the store, place orders, and add items to their shopping basket as long as there is sufficient quantity in stock. 
Users can view the total price of their order and have the option to modify it.

The main goal of this project was to create a simple app that combines the __backend__ and __frontend__ into one project. 
For the backend, we used a __MySQL database__ to store the data, the __Flask framework__ in Python to create a localhost server and route pages, 
and __Jinja2__ to pass variables from the Python code to the HTML and to create __blocks of HTML code__ that can be used anywhere.

As for the frontend, __HTML__ is used to structure and organize the content of the web page, 
__CSS__ is used to style and enhance the visual appearance of the page, 
and __JavaScript__ is used to add interactivity and functionality to the page. 

__Flask__ is a micro web framework written in Python that provides useful tools and features for building web applications. 
It includes a __lightweight server__ and the ability to connect to a database, among other things. 

__Jinja2__ is a templating engine for Python that allows developers to generate HTML or other markup code from templates and data. 
It allows you to __insert dynamic content into a template__ and keep the presentation separate from the application logic.


## Database Design
![Database](https://github.com/GCipry3/ClothesStore/blob/main/docs/database.png)


## How to navigate through the website
### 1.To reset the database to the default setup, go to the header and select __Delete Tables__
![Header](https://github.com/GCipry3/ClothesStore/blob/main/docs/header.png)

### 2.Then we have to create the tables also from the header

### 3.We have to create a new customer
* To do that we must go to our customers page
* The customer page allows us to create, view, and update customer information in the database
* Then we can easily create a __new customer__ from the top right form
![Customers](https://github.com/GCipry3/ClothesStore/blob/main/docs/customers.png)
* If we want to make any chamges to any customer we can do that by typing the customer id in the __Update Customer__ form

### 4.Add Some Products into the database
* To perform this we must go into our products page
* There we can find an __Add Product__ form in the top right
![Products](https://github.com/GCipry3/ClothesStore/blob/main/docs/products.png)

### 5.The last step is to place an order
* We have to navigate to the __Orders__ page
* The orders page allows us to create, view, and update orders and the products in each order
![Orders](https://github.com/GCipry3/ClothesStore/blob/main/docs/orders.png)
* After that we can enter into the __Basket__ of that order from the basket form
![Basket](https://github.com/GCipry3/ClothesStore/blob/main/docs/basket.png)
* Here we can add ,remove or update existing products in the basket


## The website allows us to insert some default data or to delete the existing data
* To perform this we can enter into the __Tables__ dropdown list from the header and press __Insert Data__ or __Delete Data__
![Header](https://github.com/GCipry3/ClothesStore/blob/main/docs/header.png)



## How to start the project
* We utilized a Python virtual environment for this project to keep the dependencies for this project separate from the rest of the computer

### __To set up the project, follow these steps:__

1.Set up an Ubuntu distribution.

2.Activate the virtual environment by running source "__.venv/bin/activate__".

3.Install the project dependencies by running "__pip install -r requirements.txt__".

4.Set the FLASK_APP environment variable to main by running export "__FLASK_APP=main__".

5.Start the server by running "__flask run__".
