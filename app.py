from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os


app = Flask(__name__)
app.static_folder = 'static'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Set up MongoDB Atlas connection (replace with your connection string)
uri = "mongodb+srv://unseencoderz:mongo%402213591@cluster0.pfkqmli.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.get_database("studentdata")

allowed_email_domains = ['gmail.com', 'yahoo.com', 'outlook.com']


@app.route('/')
def index():
    collection = db['mycollection']
    entries = collection.find()
    return render_template('index.html', entries=entries)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')

    domain = email.split('@')[-1]

    if domain not in allowed_email_domains:
        return "Invalid email type. Only Gmail,Yahoo and Outlook are allowed. "

    collection = db['mycollection']
    data = {'name': name, 'email': email}
    collection.insert_one(data)

    return redirect(url_for('index'))

@app.route('/uploads/<filename>', methods=['GET'])
def download_file(filename):
    # Retrieve data from MongoDB
    collection = db['mycollection']
    data = collection.find_one({'name': filename})

    if data:
        # Create a .txt file with the data and send it for download
        txt_data = f"Name: {data['name']}\nEmail: {data['email']}"
        response = make_response(txt_data)
        response.headers["Content-Disposition"] = f"attachment; filename={filename}.txt"
        response.headers["Content-type"] = "text/plain"
        return response
    else:
        return "Data not found"

if __name__ == '__main__':
    app.run(debug=True)