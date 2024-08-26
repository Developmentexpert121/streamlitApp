from flask import Flask, redirect, url_for, session,request
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.client import OAuth
import os
from dotenv import load_dotenv
from config import Config
from flask_migrate import Migrate
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from flask import jsonify
import urllib.parse


app = Flask(__name__)
app.config.from_object(Config)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
oauth = OAuth(app)
migrate = Migrate(app, db)
mail = Mail(app)


load_dotenv()
google = oauth.remote_app(
    'google',
    consumer_key=os.getenv('GOOGLE_ID'),
    consumer_secret=os.getenv('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_method='POST',
)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(100))
    last_name= db.Column(db.String(100))
    email= db.Column(db.String(100))
    name=db.Column(db.String(100))
    
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('google_token')
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')
    user_email = urllib.parse.quote(user_info.data["email"])
    return redirect(f'https://appapp-kwdxuvkdyn3eihnhzwraju.streamlit.app/?user_email={user_email}')

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return 'File uploaded successfully'

@app.route('/contact', methods=['POST'])
def contact():
    # Ensure the request contains the file
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    name = request.form.get('name')
    subject = request.form.get('subject')
    email = request.form.get('email')
    message = request.form.get('message')

    # Check if all required fields are present
    if not all([name, email, message, subject]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Create the email message
        msg = Message(
            subject=subject,
            sender=app.config['MAIL_USERNAME'],
            recipients=['developmentexpert121@gmail.com'],
            body=f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}'
        )

        # Add the file attachment if it exists
        if file and file.filename:
            msg.attach(file.filename, file.content_type, file.read())

        # Send the email
        mail.send(msg)
        return jsonify({'success': 'Email sent successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    
    app.run(debug=True)
