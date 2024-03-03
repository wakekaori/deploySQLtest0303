from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from pytz import timezone


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dbuser:DBuserpass1!@localhost/dbuser?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    # date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone('Asia/Tokyo')))
    # date = db.Column(db.DateTime, default=datetime.now(timezone('Asia/Tokyo')))
    date = db.Column(db.DateTime, default=datetime.now)
    
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname        

class ResistrationForm(FlaskForm):
    firstname = StringField('苗字')
    lastname = StringField('名前')
    submit = SubmitField('Apply')

@app.route('/',methods=['GET', 'POST'])
def index():
    form = ResistrationForm()
    users = User.query.order_by(User.id).all()
    if form.validate_on_submit():
        user = User(firstname=form.firstname.data,lastname=form.lastname.data)
        with app.app_context():
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('db_display.html', form=form, users=users)


if __name__ == '__main__':
    app.run(debug=True)