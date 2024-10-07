# simple_app/models.py
from supabase import create_client, Client
import os

# Initialize Supabase client
url = os.getenv("SUPABASE_URL")  # Set this in your environment variables
key = os.getenv("SUPABASE_KEY")  # Set this in your environment variables
supabase: Client = create_client(url, key)

class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def create(cls, name):
        data = {"name": name}
        response = supabase.table("users").insert(data).execute()
        return cls(response.data[0]['id'], name)

    @classmethod
    def get_all(cls):
        response = supabase.table("users").select("*").execute()
        return [cls(user['id'], user['name']) for user in response.data]