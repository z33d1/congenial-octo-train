from application import db
from application.models.models import UserModel, UserAppCode


def setup_auth_db():
    db.create_all()

    db.session.add(UserModel(login="dkiz",
                             password=UserModel.generate_hash('qwerty'),
                             role='admin'
                             ))
    db.session.add(UserModel(login="dkiz2",
                             password=UserModel.generate_hash('qwerty2')))
    db.session.commit()


def clear_auth_db():
    engine = db.engine
    UserModel.__table__.drop(engine)
    UserAppCode.__table__.drop(engine)