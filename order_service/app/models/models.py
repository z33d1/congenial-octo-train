from app import db
# from app.exceptions import NoRentException
from datetime import datetime

class OrderModel(db.Model):

    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    card_id = db.Column(db.Integer, nullable=False)
    # time_of_creating = db.Column(db.DateTime, nullable=True)

    def to_json(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'card_id': self.card_id             
                }

    @staticmethod
    def get_all_orders():
        return OrderModel.query.all()
        
    @staticmethod
    def get_orders_for_user(user_id):
        return OrderModel.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_order_for_user_by_id(user_id, order_id):
        return OrderModel.query.filter_by(user_id=user_id).\
            filter_by(id=order_id).first()

    @staticmethod
    def create_order(user_id, card_id):
        """
        Method to create rent record in table 'rents'
        :param user_id:
        :param card_id:
        :return: id of created order
        """

        o_m = OrderModel(user_id=user_id, card_id=card_id)

        db.session.add(o_m)
        db.session.commit()

        db.session.refresh(o_m)

        return o_m.id

    @staticmethod
    def delete_order(order_id):
        """
        Method to delete order record from table 'order'
        :param order_id:
        :return:
        """

        order_obj = OrderModel.query.filter_by(id=order_id).first()
        print(order_id)
        if order_obj is None:
            raise NoRentException(f'Order with id: {order_id} not found')
        else:
            db.session.delete(order_obj)
            db.session.commit()


    @staticmethod
    def delete_all_orders(user_id):
        order_obj = OrderModel.query.filter_by(user_id=user_id).all()
        if order_obj is None:
            raise NoOrderException(f'Orders with user_id: {order_id} not found')
        else:
            for obj in order_obj:
                db.session.delete(obj)
            db.session.commit()

