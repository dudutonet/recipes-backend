from sql_alchemy import database

class IngredientModel (database.Model):
    
    __tablename__ = 'ingredients'
    id = database.Column(database.Integer, primary_key = True)
    name: database.Column(database.String(50));
    quantity: database.Column(database.Integer);
    unit: database.Column(database.String(15));
    recipe = database.Column('recipe_id', database.Integer, database.ForeignKey('recipe.recipe_id')),
    
    def __init__(self, id, name, quantity, unit):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.unit = unit
        
    def json(self):
        return {'id' : self.id,
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
        id = database.engine.execute("select max('id') as new_id from ingredients").fetchone() 
        
        if id:
            return id['new_id'] + 1
        return 1