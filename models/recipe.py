from sql_alchemy import database

class RecipeModel (database.Model):
    
    __tablename__ = 'recipes'
    id = database.Column(database.Integer, primary_key = True)
    name = database.Column(database.String(50))
    email = database.Column(database.String(50)) #database.Float(precision=1)
    duration = database.Column(database.Integer)

    def __init__(self, id, name, rating, duration):
        self.id = id
        self.name = name
        self.rating = rating
        self.duration = duration

    def json(self):
        return {'id' : self.id,
        'name' : self.name,
        'rating' : self.rating,
        'duration' : self.duration}

    @classmethod  
    def find_movie_by_id(cls, id): #metodo de classe, mesmo que chamar Movie.query
        
        movie = cls.query.filter_by(id = id).first() # select * from movie where id = 1
        if movie:
            return movie
        return None

    def save_movie(self): 
        database.session.add(self)
        database.session.commit()

    def update_movie(self, name, rating, duration): 
        self.name = name
        self.rating = rating
        self.duration = duration

    def delete_movie(self): 
        database.session.delete(self)
        database.session.commit()
    

    @classmethod
    def find_last_movie(cls):
        # movie_id = database.engine.execute("select nextval('movie_id') as new_id").fetchone() - postgres
        
        movie_id = database.engine.execute("select max('id') as new_id from movies").fetchone() # adaptação para o mysql, vamos utilizar o campo autoincremento no futuro
        
        if movie_id:
            return movie_id['new_id'] + 1
        return 1