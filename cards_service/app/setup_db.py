from app import db
from app.models.models import CardModel

def setup_cards_db():
    db.create_all()
    for i in range(245):
        db.session.add(CardModel(name=f'UFC {245 - i}'))

    db.session.commit()
    print("DB {} set up!".format(CardModel.__table__))

def drop_cards_db():
    engine = db.engine
    CardModel.__table__.drop(engine)
    print("DB {} dropped!".format(CardModel.__table__))