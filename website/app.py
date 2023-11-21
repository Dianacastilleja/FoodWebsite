from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy


# Define a dictionary to simulate user settings (replace with database interaction).
user_settings = {
    "name": "",
    "email": "",
    "password": "",
    "phone": "",
    "creditCard": "",
    "address": "",
    "licensePlate": "",
    "past_orders": ["","",""],
    "favorite_restaurants": ["","",""]
}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db = SQLAlchemy(app)


class Visitor(db.Model):
    name = db.Column(db.String(100),default="name")
    #rewards = []
    email = db.Column(db.String(100),default="mail")
    password = db.Column(db.String(100),default="password")
    phone = db.Column(db.Integer, default=1, primary_key=True)
    creditCard = db.Column(db.Integer,default=1)
    address = db.Column(db.String(100),default="street" )

    def __repr__(self):
        return f"{self.name}"



# Route for the welcome page
@app.route('/')
def welcome():
    signedIn = False

    if user_settings["name"] != "":
        signedIn = True
    name = user_settings["name"]
    return render_template('welcome.html',name=name,signedIn = signedIn)


@app.route('/map')
def map():
    pickUp = "UTRGV"
    dropOff = user_settings["address"]
    #dropOff = "art street"
    return render_template('map.html', pickUp = pickUp, dropOff=dropOff)


# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    notInDB = False
    wrongPass = False


    if request.method == 'POST':
        phone=request.form['phone']
        password=request.form['password']

        visitor = Visitor.query.filter_by(phone=phone).first()

        if (visitor == None):
            notInDB = True
            wrongPass = False

        elif(visitor.password == password):
            user_settings['name'] = visitor.name
            user_settings['email'] = visitor.email
            user_settings['phone'] = visitor.phone
            user_settings['creditCard'] = visitor.creditCard
            user_settings['address'] = visitor.address 
            return redirect("/")        
        
        else:#(visitor.password != password)
            notInDB = False
            wrongPass = True

    return render_template('login.html',wrongPass=wrongPass,notInDB=notInDB)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    taken = False
    visitor = None
    

    if request.method == 'POST':
        first=request.form['first']
        last=request.form['last']
        email=request.form['email']
        password=request.form['password']
        phone=request.form['phone']
        credit=request.form['credit']
        address = request.form['address']
        
        #check if user is already in database
        visitor = Visitor.query.filter_by(phone=phone).first()
        #visitor = Visitor.query.get(phone)

        if (visitor == None):
            visitor = Visitor(name = first + " " + last,email=email,phone=phone,creditCard=credit,password = password,address=address)
            db.session.add(visitor)
            db.session.commit()
            return redirect('/login')
        else:
            taken = True
    
    return render_template('signup.html',taken=taken)

@app.route('/driver_registration', methods=['GET', 'POST'])
def driver_signup():

    notInDB = False
    wrongPass = False


    if request.method == 'POST':
        phone=request.form['phone']
        password=request.form['password']
        licensePlate = request.form['licensePlate']

        visitor = Visitor.query.filter_by(phone=phone).first()

        if (visitor == None):
            notInDB = True
            wrongPass = False

        elif(visitor.password == password):
            visitor.licensePlate = licensePlate
            db.session.commit()
            return redirect('/login')       
        
        else:#(visitor.password != password)
            notInDB = False
            wrongPass = True

    return render_template('driver_registration.html',wrongPass=wrongPass,notInDB=notInDB)


@app.route('/driver_register', methods=['POST'])
def driver_register():
    # Process the driver registration form data, validate it, and store it in your database
    # You will use request.form to access the form data
    # Example code to handle the form submission
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    driver_license = request.form['driver_license']
    account_number = request.form['account_number']
    routing_number = request.form['routing_number']

    # Assuming successful registration, you may want to redirect to a success page
    return redirect('/success')


@app.route('/settings',methods=['GET','POST'])
def settings():
    phone = user_settings["phone"]
    visitor = Visitor.query.filter_by(phone=phone).first()
    if request.method == 'POST':
        new_payment_method = request.form.get('new_payment_method')
        new_address = request.form.get('new_address')
        new_email = request.form.get('new_email')

        if new_payment_method:
            user_settings["creditCard"] = new_payment_method
            #Visitor.query.filter_by(phone=phone).first().creditCard = new_payment_method
            visitor.creditCard = new_payment_method
            db.session.commit()
        if new_address:
            user_settings['address'] = new_address
            #Visitor.query.filter_by(phone=phone).first().address = new_address
            visitor.address = new_address
            db.session.commit()
        if new_email:
            user_settings["email"] = new_email
            #Visitor.query.filter_by(phone=phone).first().email = new_email
            visitor.email = new_email
            db.session.commit()
        


    # Render the settings page and pass user settings to the template
    return render_template('settings.html', user_settings=user_settings)



@app.route('/update_email', methods=['POST'])
def update_email():
    new_email = request.form['new_email']
    
    # Update the email address in the database or dictionary
    user_settings['email'] = new_email
    
    return redirect('/settings')


@app.route('/update_address', methods=['POST'])
def update_address():
    new_address = request.form['new_address']
    
    # Update the home address in the database or dictionary
    user_settings['address'] = new_address
    
    return redirect('/settings')

@app.route('/update_payment', methods=['POST'])
def update_payment():
    new_payment_method = request.form['new_payment_method']
    
    # Update the payment method in the database or dictionary
    user_settings['payment_method'] = new_payment_method
    
    return redirect('/settings')

@app.route('/update_contact_preference', methods=['POST'])
def update_contact_preference():
    new_contact_preference = request.form['new_contact_preference']
    
    # Update the contact preference in the database or dictionary
    user_settings['contact_preference'] = new_contact_preference
    
    return redirect('/settings')



# Route for All Restaurants
ordered_items = []
#Chick Fil A
@app.route('/R1', methods=['GET', 'POST'])
def R1():
    if request.method == 'POST':
        food_item = request.form['food_item']
        price = float(request.form['price'])

        ordered_items.append({
            'food_item': food_item,
            'price': price
        })

    return render_template('R1.html', user_settings=user_settings, ordered_items=ordered_items)

# # Route for submitting the order
# @app.route('/submit_order', methods=['POST'])
# def submit_order():
#     # Assuming you want to perform some action when the order is submitted
#     # For now, let's print the ordered items and total price to the console
#     for item in ordered_items:
#         print(f"Price: ${item['price']}")


#Jack In The Box
@app.route('/R2',  methods=['GET', 'POST'])
def R2():
    if request.method == "POST":
        food_item = request.form["food_item"]
        price = float(request.form['price'])

        ordered_items.append({
            'food_item': food_item,
            'price': price
        })
    return render_template('R2.html', user_settings=user_settings)

#Pizza Hut
@app.route('/R3', methods=['GET', 'POST'])
def R3():
    if request.method == 'POST':
        food_item = request.form['food_item']
        price = float(request.form['price'])

        ordered_items.append({
            'food_item': food_item,
            'price': price
        })
    return render_template('R3.html', user_settings=user_settings)

# Route for submitting the order
@app.route('/submit_order', methods=['POST'])
def submit_order():
    # Assuming you want to perform some action when the order is submitted
    # For now, let's print the ordered items and total price to the console
    for item in ordered_items:
        print(f"Price: ${item['price']}")

    total_price = sum(item['price'] for item in ordered_items)
    print(f"Total Price: ${total_price}")

    # Clear the ordered_items list for the next order
    ordered_items.clear()
    return redirect('/success')  # Redirect to a success page or any other desired page after submitting the order

# Route for the success page
@app.route('/success')
def success():
    return render_template('success.html')


# Route for the checkout page
@app.route('/checkout')
def checkout():
    total_price = sum(item['price'] for item in ordered_items)
    return render_template('checkout.html', ordered_items=ordered_items, total_price=total_price)

# Route for the orders page
@app.route('/orders')
def orders():
    return render_template('orders.html',all_orders = ordered_items)


# Display all Orders
def displayOrders():
    pass

with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
    app.run(debug=True)
