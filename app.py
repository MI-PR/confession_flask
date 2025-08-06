from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get credentials from .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        confession = request.form['confession']
        if confession.strip():
            supabase.table('confessions').insert({"message": confession}).execute()
            return redirect(url_for('show_confession'))
        else:
            return redirect(url_for('submit_form'))
    return render_template('submit.html')

@app.route('/confessions')
def show_confession():
    response = supabase.table('confessions').select('message').order('id', desc=True).execute()
    confessions = [item['message'] for item in response.data]
    return render_template('confessions.html', confessions=confessions)

if __name__ == '__main__':
    app.run(debug=True)

