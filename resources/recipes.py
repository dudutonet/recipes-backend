from flask_restful import Resource, reqparse, request
from models.recipe import RecipeModel
from models.ingredient import IngredientModel
from flask_jwt_extended import jwt_required, get_jwt_identity

ingredient_request = reqparse.RequestParser()
ingredient_request.add_argument('name', type=str, required=True, help="ingredient name is required")

my_request = reqparse.RequestParser()
my_request.add_argument('name', type=str, required=True, help="email is required")
my_request.add_argument('description', type=str, required=True, help="Descriotion is required")
my_request.add_argument('howToMake', type=str, required=True, help="How to make is required")
my_request.add_argument('cookTime', type=str, required=False, help="Cook Time is required")
my_request.add_argument('photoUrl', type=str, required=True, help="photo is required")
my_request.add_argument('revenue', type=str, required=True, help="revenue is required")
my_request.add_argument('ingredients', type=list, location="json", action='append', help="Ingredients are required")

class Recipes(Resource):
    def get(self):
        return {'recipes' : [recipe.json([]) for recipe in RecipeModel.query.all()]}

class Recipe(Resource):

    def get(self, id):
        recipe = RecipeModel.find_recipe_by_id(id)
        ingredients = IngredientModel.find_ingredient_by_recipe_id(id)
        if recipe:
            return recipe.json(ingredients)
        return {'message':'recipe not found'}, 200

    @jwt_required()
    def post(self, id):
        recipe_id = RecipeModel.find_last_recipe()
        dados = my_request.parse_args()
        converted_data = {
            "name": dados['name'],
            "description": dados['description'],
            "how_to_make": dados['howToMake'],
            "cook_time": dados['cookTime'],
            "revenue": dados['revenue'],
            "photo_url": dados['photoUrl'],
            "user": get_jwt_identity()
        }

        new_recipe = RecipeModel(recipe_id, **converted_data)
        
        new_ingredients = []
        
        try:
            new_recipe.user = get_jwt_identity()
            new_recipe.save_recipe()
            for ingredient in request.get_json()['ingredients']:
                ingredient_id = IngredientModel.find_last_ingredient()
                name = ingredient['name']
                quantity = ingredient['quantity']
                unit = ingredient['unit']
                print('alo')
                new_ingredient = IngredientModel(ingredient_id, name, quantity, unit, recipe_id)
                print('dps')
                new_ingredient.save_ingredient()
                new_ingredients.append(new_ingredient)

        except:
            return {'message':'An internal error ocurred.'}, 500

        return new_recipe.json(new_ingredients), 201

    @jwt_required()
    def put(self, id):
        dados = my_request.parse_args()
        recipe = RecipeModel.find_recipe_by_id(id)
        if recipe:
            recipe.update_recipe(dados['name'], dados['description'], dados['howToMake'], dados['cookTime'], dados['revenue'], dados['photoUrl'])
            recipe.save_recipe()
            return recipe.json(), 200

        recipe_id = RecipeModel.find_last_recipe()
        new_recipe = RecipeModel(recipe_id, **dados)
        new_recipe.save_recipe()
        
        return new_recipe.json(), 201

    @jwt_required()
    def delete(self, id):
        recipe = RecipeModel.find_recipe_by_id(id)
        if recipe:
            recipe.delete_recipe()
            return {'message' : 'Recipe deleted.'}
        return {'message' : 'recipe not founded'}, 204
    
