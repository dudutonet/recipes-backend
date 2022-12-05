from sql_alchemy import database

class IngredientModel (database.Model):
    
    __tablename__ = 'ingredients'
    ingredient_id = database.Column(database.Integer, primary_key = True)
    name = database.Column(database.String(50));
    quantity = database.Column(database.Integer);
    unit = database.Column(database.String(15));
    recipe_id = database.Column('recipe_id', database.Integer, database.ForeignKey('recipes.recipe_id'))

    def __init__(self, ingredient_id, name, quantity, unit, recipe_id):
        print('dentro')
        self.ingredient_id = ingredient_id
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.recipe_id = recipe_id
        
    def json(self):
        return {'id' : self.ingredient_id,
        'name' : self.name,
        'quantity' : self.quantity,
        'howToMake' : self.howToMake
    }

    @classmethod  
    def find_ingredient_by_id(cls, id):
        ingredient = cls.query.filter_by(id = id).first()
        if ingredient:
            return ingredient
        return None

    @classmethod  
    def find_ingredient_by_recipe_id(cls, recipe_id):
        ingredient = cls.query.filter_by(recipe_id = recipe_id).first()
        if ingredient:
            return ingredient
        return None

    def save_ingredient(self): 
        database.session.add(self)
        database.session.commit()

    def update_ingredient(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    def delete_ingredient(self): 
        database.session.delete(self)
        database.session.commit()

    @classmethod
    def delete_all_by_recipe(recipe_id):
        database.engine.execute("delete from ingredients where recipe_id = " + recipe_id)
        database.session.commit()
    
    

    @classmethod
    def find_last_ingredient(cls):        
        id = database.engine.execute("select max(ingredient_id) as new_id from ingredients").fetchone() 
        
        if id[0]:
            return id[0] + 1
        return 1