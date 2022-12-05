from flask_restful import Resource, reqparse
from models.recipe import RecipeModel
from models.ingredient import IngredientModel
from flask_jwt_extended import jwt_required, get_jwt_identity

my_request = reqparse.RequestParser()
my_request.add_argument('id', type=str, required=True, help="login is required")
my_request.add_argument('name', type=str, required=True, help="email is required")
my_request.add_argument('description', type=str, required=True, help="Descriotion is required")
my_request.add_argument('howToMake', type=str, required=True, help="How to make is required")
my_request.add_argument('cookTIme', type=str, required=False, help="password is required")
my_request.add_argument('photoUrl', type=str, required=True, help="photo is required")
my_request.add_argument('ingredients', type=list, required=True, help="Ingredients are required")

class Recipes(Resource):
    def get(self):
        return {'recipes' : [recipe.json() for recipe in RecipeModel.query.all()]}

class Recipe(Resource):

    def get(self, id):
        recipe = RecipeModel.find_recipe_by_id(id)
        if recipe:
            return recipe.json()
        return {'message':'recipe not found'}, 200

    @jwt_required()
    def post(self, id):
        recipe_id = RecipeModel.find_last_recipe()
        dados = Recipe.my_request.parse_args()
        new_recipe = RecipeModel(recipe_id, **dados)
        
        try:
            new_recipe.user = get_jwt_identity()
            new_recipe.save_recipe()
            for ingredient in dados['ingredients']:
                ingredient_id = IngredientModel.find_last_ingredient()
                new_ingredient = IngredientModel(ingredient_id, **ingredient)
                new_ingredient.save_ingredient()
        except:
            return {'message':'An internal error ocurred.'}, 500

        return new_recipe.json(), 201

    @jwt_required()
    def put(self, id):
        dados = Recipe.my_request.parse_args()
        recipe = RecipeModel.find_recipe_by_id(id)
        if recipe:
            recipe.update_recipe(**dados)
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
    
