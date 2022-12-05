from sql_alchemy import database

class RecipeModel (database.Model):
    
    __tablename__ = 'recipes'
    recipe_id = database.Column(database.Integer, primary_key = True)
    name = database.Column(database.String(50))
    description = database.Column(database.String(4000))
    how_to_make = database.Column(database.String(6000))
    cook_time = database.Column(database.String(50))
    revenue = database.Column(database.Integer)
    photo_url = database.Column(database.String(1000))
    user_id = database.Column('user_id', database.Integer, database.ForeignKey('users.user_id'))

    def __init__(self, recipe_id, name, description, how_to_make, cook_time, revenue, photo_url, user):
        self.recipe_id = recipe_id
        self.name = name
        self.description = description
        self.how_to_make = how_to_make
        self.cook_time = cook_time
        self.revenue = revenue
        self.photo_url = photo_url
        self.user_id = user

    def json(self, ingredients = []):
        return {'id' : self.recipe_id,
        'name' : self.name,
        'description' : self.description,
        'howToMake' : self.how_to_make,
        'cookTime' : self.cook_time, 
        'revenue' : self.revenue,
        'user' : self.user_id,
        'photoUrl': self.photo_url
    }

    @classmethod  
    def find_recipe_by_id(cls, id):
        recipe = cls.query.filter_by(recipe_id = id).first()
        if recipe:
            return recipe
        return None

    def save_recipe(self): 
        database.session.add(self)
        database.session.commit()

    def update_recipe(self, name, description, howToMake, cookTime, revenue, photoUrl):
        self.name = name
        self.description = description 
        self.how_to_make = howToMake
        self.cook_time = str(cookTime)       
        self.revenue = revenue 
        self.photo_url = photoUrl

    def delete_recipe(self): 
        database.session.delete(self)
        database.session.commit()
    

    @classmethod
    def find_last_recipe(cls):        
        id = database.engine.execute("select max(recipe_id) as new_id from recipes").fetchone() 
        
        if id[0]:
            return int(id[0]) + 1
        return 1