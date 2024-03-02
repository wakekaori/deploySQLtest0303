from main import app, db, User

with app.app_context():
    #db.drop_all()
    db.create_all()

    user1 = User('mori', 'saori')
    db.session.add(user1)
    db.session.commit()