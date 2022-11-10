from flask_restful import Resource, reqparse
from models.recipe import MovieModel
from flask_jwt_extended import jwt_required

class Movies(Resource):
    def get(self):
        return {'movies' : [movie.json() for movie in MovieModel.query.all()]}


class Movie(Resource):
    minha_requisicao = reqparse.RequestParser()
    minha_requisicao.add_argument('name', type=str, required=True, help="name is required")
    minha_requisicao.add_argument('rating')
    minha_requisicao.add_argument('duration', type=int, required=True, help="duration is required")

    @jwt_required()
    def get(self, id):
        movie = MovieModel.find_movie_by_id(id)
        if movie: #if movie is not None
            return movie.json()
        return {'message':'movie not found'}, 200 # or 204

    @jwt_required()
    def post(self, id):
        movie_id = MovieModel.find_last_movie()
        dados = Movie.minha_requisicao.parse_args()
        new_movie = MovieModel(movie_id, **dados)
        
        try:
            new_movie.save_movie()
        except:
            return {'message':'An internal error ocurred.'}, 500

        return new_movie.json(), 201

    def put(self, id):
        dados = Movie.minha_requisicao.parse_args()
        movie = MovieModel.find_movie_by_id(id)
        if movie:
            movie.update_movie(**dados)
            movie.save_movie()
            return movie.json(), 200

        movie_id = MovieModel.find_last_movie()
        new_movie = MovieModel(movie_id, **dados)
        new_movie.save_movie()
        return new_movie.json(), 201

    def delete(self, id):
        movie = MovieModel.find_movie_by_id(id)
        if movie:
            movie.delete_movie()
            return {'message' : 'Movie deleted.'}
        return {'message' : 'movie not founded'}, 204