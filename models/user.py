from sql_alchemy import database
from sqlalchemy.sql.expression import func

class UserModel (database.Model):
    
    __tablename__ = 'users'
    user_id = database.Column(database.Integer, primary_key = True)
    login = database.Column(database.String(50), unique=True)
    email = database.Column(database.String(50), unique=True)
    password = database.Column(database.String(50))
    photo_url = database.Column(database.String(500))

    def __init__(self, user_id, login, email, password, photoUrl = ""):
        self.user_id = user_id
        self.login = login
        self.email = email
        self.password = password
        self.photo_url = photoUrl

    def json(self):
        return {
            'userId' : self.user_id,
            'login' : self.login,
            'email' : self.email,
            'password': self.password,
            'photoUrl': self.photo_url
        }

    @classmethod  
    def find_user_by_id(cls, user_id): 
        user = cls.query.filter_by(user_id = user_id).first()
        if user:
            return user
        return None

    @classmethod  
    def find_user_by_login(cls, login): 
        user = cls.query.filter_by(login = login).first()
        if user:
            return user
        return None

    def save_user(self): 
        database.session.add(self)
        database.session.commit()

    def update_user(self, user_id, login, email, password, photo_url): 
        self.user_id = user_id
        self.loging = login
        self.email = email
        self.password = password
        self.photo_url = photo_url

    def delete_user(self): 
        database.session.delete(self)
        database.session.commit()
        
    @classmethod
    def find_last_user(cls):
        user_id = database.session.query(func.max(cls.user_id)).one()[0]

        if user_id:
            return user_id + 1
        return 1