from flask import Flask, render_template, request, redirect

app = Flask(__name__)

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
    
    # Perform necessary validation and database operations

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

if __name__ == '__main__':
    app.run(debug=True)
