from sql_alchemy import database

class RatingModel (database.Model):
    
    __tablename__ = 'ratings'
    id = database.Column(database.Integer, primary_key = True)
    user: database.Column(database.String(50));
    rate: database.Column(database.Integer);
    comment: database.Column(database.String(300));
    recipe_id = database.Column('recipe_id', database.Integer, database.ForeignKey('recipe.recipe_id')),
    
    def __init__(self, id, user, rate, comment):
        self.id = id
        self.user = user
        self.quantity = rate
        self.unit = comment
        
    def json(self):
        return {'id' : self.id,
        'user' : self.user,
        'rate' : self.rate,
        'comment' : self.comment
    }

    @classmethod  
    def find_rating_by_id(cls, id):
        rating = cls.query.filter_by(id = id).first()
        if rating:
            return rating
        return None

    def save_rating(self): 
        database.session.add(self)
        database.session.commit()

    def update_rating(self, user, rating, comment):
        self.name = user
        self.quantity = rating
        self.unit = comment

    def delete_rating(self): 
        database.session.delete(self)
        database.session.commit()

    @classmethod
    def delete_all_by_recipe(recipe_id):
        database.engine.execute("delete from ratings where recipe_id = " + recipe_id)
        database.session.commit()
    
    
    @classmethod
    def find_last_rating(cls):        
        id = database.engine.execute("select max('id') as new_id from ingredients").fetchone() 
        
        if id:
            return id['new_id'] + 1
        return 1