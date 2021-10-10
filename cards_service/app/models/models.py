from app import db
from app.exceptions import NoCardException

class CardModel(db.Model):
    """
    CardsModel
    """

    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    attendance = db.Column(db.Integer, default=0)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {'id': self.id,
                'Name': self.name,
                'Attendance': self.attendance
                }

    @staticmethod
    def get_all_cards():        
        return CardModel.query.all()
        # return CardModel.query.filter_by(name=name).first().to_json()
        # filter_by(app_id=app_id, user_id=user_id).first()

    @staticmethod
    def get_card(card_id):
        return CardModel.query.filter_by(id = card_id).first()

    @staticmethod
    def get_cards_w_pagination(page, per_page):
        return CardModel.query.paginate(page, per_page, False).items

    @staticmethod
    def attendance_edit(card_id, value):
        card_obj = CardModel.query.filter_by(id=card_id).first()

        if card_obj is None:
            raise NoCardException('Card with id: {} not found'.format(card_id))
        else:
            card_obj.attendance += value * 1
            db.session.commit()


    @staticmethod
    def del_card(card_id):
        """
        Method to delete card record from table 'card'
        :param card_id:
        :return:
        """

        card_obj = CardModel.query.filter_by(id=card_id).first()
        
        if card_obj is None:
            raise NoCardException('Card with id: {} not found'.format(card_id))
        else:
            db.session.delete(card_obj)
            db.session.commit()
        
