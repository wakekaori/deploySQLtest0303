from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from pytz import timezone


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dbuser:DBuserpass1!@localhost/dbuser?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    date = db.Column(db.DateTime, default=datetime.now(timezone('Asia/Tokyo')))
    
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname        

@app.route('/',methods=['GET', 'POST'])
def index():
    with app.app_context():
        if request.method == 'POST':    
            add_user = User(firstname='wake',lastname='kaori')
            db.session.add(add_user)
            db.session.commit()
            return redirect(url_for('index'))

        users = User
    return render_template('db_display.html', users=users)


if __name__ == '__main__':
    app.run(debug=True)