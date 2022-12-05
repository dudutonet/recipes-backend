from sql_alchemy import database

class RecipeModel (database.Model):
    
    __tablename__ = 'recipes'
    id = database.Column(database.Integer, primary_key = True)
    name = database.Column(database.String(50))
    description = database.Column(database.String(4000))
    howToMake = database.Column(database.String(6000))
    cook_time = database.Column(database.Integer)
    revenue = database.Column(database.Integer)
    user = database.Column(database.String(50))

    def __init__(self, id, name, description, howToMake, cook_time, revenue, user):
        self.id = id
        self.name = name
        self.description = description
        self.howToMake = howToMake
        self.cook_time = cook_time
        self.revenue = revenue
        self.user = user

    def json(self):
        return {'id' : self.id,
        'name' : self.name,
        'description' : self.description,
        'howToMake' : self.howToMake,
        'cook_time' : self.cook_time, 
        'revenue' : self.revenue,
        'user' : self.user}

    @classmethod  
    def find_recipe_by_id(cls, id): #metodo de classe, mesmo que chamar Recipe.query
        
        recipe = cls.query.filter_by(id = id).first() # select * from movie where id = 1
        if recipe:
            return recipe
        return None

    def save_recipe(self): 
        database.session.add(self)
        database.session.commit()

    def update_recipe(self, name, description, howToMake, cook_time, revenue, user): #metodo de classe, 
        self.name = name
        self.description = description 
        self.howToMake = howToMake
        self.cook_time = cook_time        
        self.revenue = revenue 
        self.user = user

    def delete_recipe(self): 
        database.session.delete(self)
        database.session.commit()
    

    @classmethod
    def find_last_recipe(cls):
        # movie_id = database.engine.execute("select nextval('movie_id') as new_id").fetchone() - postgres
        
        id = database.engine.execute("select max('id') as new_id from recipes").fetchone() # adaptação para o mysql, vamos utilizar o campo autoincremento no futuro
        
        if id:
            return id['new_id'] + 1
        return 1

class Recipe(database.Model):
    
    __tablename__ = 'recipes'
    id = database.Column(database.Integer, primary_key = True)
    name = database.Column(database.String(50))
    description = database.Column(database.String(4000))
    howToMake = database.Column(database.String(6000))
    cook_time = database.Column(database.Integer)
    revenue = database.Column(database.Integer)
    user = database.Column(database.String(50))
    user = database.relationship('User', passive_deletes=True)
    user_id = database.Column(database.Integer(),database.ForeignKey("users.id"))


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

    def get_role(self):
        return self.user

 # Define the Role data-model
class User(db.Model):
        __tablename__ = 'roles'
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)