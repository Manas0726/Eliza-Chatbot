from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'devilgaming2630@gmail.com' # enter your email address
app.config['MAIL_PASSWORD'] = 'TemPorary@2004' # enter your email password
app.config['MAIL_DEFAULT_SENDER'] = 'devilgaming2630@gmail.com' # enter your email address
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    
    if not name or not email or not message:
        return "error"
    
    try:
        msg = Message(subject=f"New Message from {name}", recipients=["devilgaming2630@gmail.com"]) # enter the email address where you want to receive the message
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        mail.send(msg)
        return "success"
    except:
        return "error"
