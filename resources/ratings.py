from flask_restful import Resource, reqparse
from models.recipe import RecipeModel
from models.rating import RatingModel
from flask_jwt_extended import jwt_required, get_jwt_identity

my_request = reqparse.RequestParser()
my_request.add_argument('rate', type=str, required=True, help="Rate is required")
my_request.add_argument('comment', type=str, required=True, help="Comment is required")
my_request.add_argument('recipe', type=list, required=True, help="Recipe are required")

class Ratings(Resource):
    def get(self):
        return {'ratings' : [rating.json() for rating in RatingModel.query.all()]}

class Rating(Resource):

    def get(self, id):
        rating = RatingModel.find_rating_by_id(id)
        if rating:
            return rating.json()
        return {'message':'rating not found'}, 200

    @jwt_required()
    def post(self, id):
        rating_id = RatingModel.find_last_rating()
        dados = Rating.my_request.parse_args()
        new_rating = RatingModel(rating_id, **dados)
        
        try:
            new_rating.user = get_jwt_identity()
            new_rating.save_rating()
            for rating in dados['ratings']:
                rating_id = RatingModel.find_last_rating()
                new_rating = RatingModel(rating_id, **rating)
                new_rating.save_ingredient()
        except:
            return {'message':'An internal error ocurred.'}, 500

        return new_rating.json(), 201

    @jwt_required()
    def put(self, id):
        dados = Rating.my_request.parse_args()
        rating = RatingModel.find_rating_by_id(id)
        if rating:
            rating.update_rating(**dados)
            rating.save_rating()
            return rating.json(), 200

        rating_id = RatingModel.find_last_rating()
        new_rating = RatingModel(rating_id, **dados)
        new_rating.save_rating()
        
        return new_rating.json(), 201

    @jwt_required()
    def delete(self, id):
        rating = RatingModel.find_rating_by_id(id)
        if rating:
            rating.delete_rating()
            return {'message' : 'Rating deleted.'}
        return {'message' : 'rating not founded'}, 204
    
