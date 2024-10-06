from flask import Flask, request, render_template, redirect
from dotenv import load_dotenv
import os
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Create a new route to handle username input
# @app.route('/add_username', methods=['GET', 'POST'])
# def add_username():
#     if request.method == 'POST':
#         username = request.form['username']
#         # Store the username in Supabase
#         data = {"username": username}
#         supabase.table("users").insert(data).execute()
#         return redirect('/user_list')
#     return render_template('add_username.html')

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

# Create a new route to display the list of usernames
@app.route('/user_list')
def user_list():
    response = supabase.table("users").select("username").execute()
    usernames = response.data
    return render_template('user_list.html', usernames=usernames)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
