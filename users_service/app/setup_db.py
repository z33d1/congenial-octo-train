from app import db
from app.models.models import UserModel


def setup_users_db():
    db.create_all()

    db.session.add(UserModel(username='Kizilov D.'))
    db.session.add(UserModel(username='Michael Bale'))
    db.session.add(UserModel(username='Rock'))
    db.session.add(UserModel(username='Paper'))
    db.session.add(UserModel(username='Scissors'))

    db.session.commit()


def clear_users_db():
    engine = db.engine
    UserModel.__table__.drop(engine)