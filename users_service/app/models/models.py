from app import db

class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)

    def to_json(self):
        return {'id': self.id,
                'username': self.username}

    @staticmethod
    def get_user_info_by_id(user_id):
        """
        Method to get user info (id, name)
        :param user_id:
        :return UserModel
        """        
        return UserModel.query.filter_by(id = user_id).first()

    @staticmethod
    def get_users():
        """
        Method to get users info (id, name)
        :param user_id:
        :return UserModel
        """        
        return UserModel.query.all()


    def __repr__(self):
        return '<User: {} with id: {}>'.format(self.username, self.id)
