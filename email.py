from flask import Flask, current_app
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "@gmail.com"
app.config['MAIL_PASSWORD'] = ""

mail = Mail(app)
with app.app_context():
    msg = Message()
    msg.sender = '@gmail.com'
    msg.subject = "Email do Vasco :BOT:"
    msg.recipients = []
    
    msg.html = '''<style>
    .a img{
        display: inline-block;
    }
    h1{
        text-align: center;
        color: blueviolet;
    }
    h2{
        text-align: center;
    }h3{
        text-align: center;
    }
    b{
        font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    }
</style>
<body>
    <h1>Bom dia Sr.</h1>
    <h2>Por obséquio, compareça a sede do <b>GIGANTE DA COLINA para efetuar a sua contratação efetiva.</b></h2>
    <h3>Assinado, Eurico Miranda.</h3>
</body>'''
    mail.send(msg)
