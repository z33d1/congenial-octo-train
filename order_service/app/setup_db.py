from app import db
from app.models.models import OrderModel

def setup_orders_db():
    db.create_all()
    db.session.commit()
    print("DB {} set up!".format(OrderModel.__table__))

def drop_orders_db():
    engine = db.engine
    OrderModel.__table__.drop(engine)
    print("DB {} dropped!".format(OrderModel.__table__))