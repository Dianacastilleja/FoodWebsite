from flask import Flask, render_template, request, redirect

app = Flask(__name__)

ordered_items = []

# Define a dictionary to simulate user settings (replace with database interaction).
user_settings = {
    "email": "user@example.com",
    "address": "123 Main St",
    "payment_method": "Credit Card",
    "contact_preference": "Email",
    "past_orders": ["Order 1", "Order 2", "Order 3"],
    "favorite_restaurants": ["Restaurant A", "Restaurant B", "Restaurant C"],
}

# Route for the welcome page
@app.route('/')
def welcome():
    return render_template('welcome.html')

# Route for the login page
@app.route('/login')
def login():
    return render_template('login.html')

# Route for the signup page
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/driver_signup')
def driver_signup():
    return render_template('driver_signup.html')

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


@app.route('/settings')
def settings():
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

# Revolution Noodle


# Route for the checkout page
@app.route('/checkout')
def checkout():
    total_price = sum(item['price'] for item in ordered_items)
    return render_template('checkout.html', ordered_items=ordered_items, total_price=total_price)

if __name__ == '__main__':
    app.run(debug=True)
