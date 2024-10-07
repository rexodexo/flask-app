from flask import Flask, request, render_template, redirect, url_for, session, flash
from dotenv import load_dotenv
import os
import traceback
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set the secret key for the Flask application
app.secret_key = os.getenv("SECRET_KEY")

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', user=session['user'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            app.logger.info(f"Attempting login for email: {email}")
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            app.logger.info(f"Login response: {response}")
            if response.user:
                # Store only the user ID and email in the session
                session['user'] = {
                    'id': response.user.id,  # Assuming response.user has an 'id' attribute
                    'email': response.user.email  # Assuming response.user has an 'email' attribute
                }
                return redirect(url_for('index'))
            else:
                flash("Invalid email or password.", 'error')
        except Exception as e:
            app.logger.error(f"Login error: {str(e)}")
            app.logger.error(traceback.format_exc())
            flash(str(e), 'error')
        return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    if password != confirm_password:
        flash("Passwords don't match!", 'error')
        return render_template('login.html')
    
    try:
        app.logger.info(f"Attempting signup for email: {email}")
        response = supabase.auth.sign_up({"email": email, "password": password})
        app.logger.info(f"Signup response: {response}")
        if response.user:
            flash("Sign up successful! Please check your email to verify your account.", 'success')
        else:
            flash("Failed to sign up. Please try again.", 'error')
    except Exception as e:
        app.logger.error(f"Signup error: {str(e)}")
        app.logger.error(traceback.format_exc())
        flash(str(e), 'error')
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.pop('user', None)
        return redirect(url_for('login'))
    # ... existing code ...

if __name__ == '__main__':
    app.run(debug=True)
    
# Home route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_username', methods=['GET', 'POST'])
def add_username():
    if request.method == 'POST':
        username = request.form['username']
        # Store the username in Supabase
        data = {"username": username}
        response = supabase.table("users").insert(data).execute()
        
        print("Response:", response)  # Print the entire response object for debugging
        
        return redirect('/user_list')
    return render_template('add_username.html')

@app.route('/add_email', methods=['GET', 'POST'])
def add_email():
    if request.method == 'POST':
        email = request.form['email']
        # Store the email in Supabase
        data = {"email": email}
        response = supabase.table("users").insert(data).execute()
        
        print("Response:", response)  # Print the entire response object for debugging
        
        return redirect('/user_list')
    return render_template('add_email.html')

# Create a new route to display the list of usernames
@app.route('/user_list')
def user_list():
    response = supabase.table("users").select("username").execute()
    usernames = response.data
    return render_template('user_list.html', usernames=usernames)

if __name__ == '__main__':
    app.run(debug=True)  # Add debug=True here to enable debug mode
