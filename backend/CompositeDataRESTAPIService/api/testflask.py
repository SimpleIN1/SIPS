from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.mail.ru'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'testemail.emal@mail.ru'
app.config['MAIL_PASSWORD'] = 'dGOyU5LbGH10P20RGpgj'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


@app.route("/")
def index():
    msg = Message(subject='Hello from the other side!', sender='testemail.emal@mail.ru', recipients=['gorgh31@mail.ru'])
    msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works."
    mail.send(msg)
    return "Message sent!"


if __name__ == '__main__':
    app.run(debug=True)