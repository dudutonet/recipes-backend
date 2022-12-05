from sql_alchemy import database
from sqlalchemy.sql.expression import func


class UserModel (database.Model):
    
    __tablename__ = 'users'
    user_id = database.Column(database.Integer, primary_key = True)
    email = database.Column(database.String(50))
    cell_phone = database.Column(database.String(20))
    password = database.Column(database.String(50))
    photo_url = database.Column(database.String(500))
    user_type = database.Column(database.String(15))
    created_date = database.Culumn(database.DateTime)
    updated_date = database.Culumn(database.DateTime)

    def __init__(self, user_id, email, cell_phone, user_type, password):
        self.user_id = user_id
        self.email = email
        self.cell_phone = cell_phone
        self.user_type = user_type
        self.password = password

    def json(self):
        return {
            'user_id' : self.user_id,
            'email' : self.email,
            'cell_phone': self.cell_phone,
            'user_type': self.user_type,
            
        }

    @classmethod  
    def find_user_by_id(cls, user_id): 
        user = cls.query.filter_by(user_id = user_id).first()
        if user:
            return user
        return None

    @classmethod  
    def find_user_by_email(cls, email): 
        user = cls.query.filter_by(email = email).first()
        if user:
            return user
        return None

    def save_user(self): 
        database.session.add(self)
        database.session.commit()

    def update_user(self, user_id, email, cell_phone, password): 
        self.user_id = user_id
        self.email = email
        self.cell_phone = cell_phone
        self.password = password

    def delete_user(self): 
        database.session.delete(self)
        database.session.commit()
        
    @classmethod
    def find_last_user(cls):
        # user_id = database.engine.execute("select nextval('user_id') as new_id").fetchone() - postgres
        user_id = database.session.query(func.max(cls.user_id)).one()[0]

        if user_id:
            return user_id + 1
        return 1