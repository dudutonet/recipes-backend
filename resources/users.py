from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token

my_login_request = reqparse.RequestParser()
my_login_request.add_argument('login', type=str, required=True, help="login is required")
my_login_request.add_argument('password', type=str, required=True, help="password is required")

my_user_request = reqparse.RequestParser()
my_user_request.add_argument('login', type=str, required=True, help="login is required")
my_user_request.add_argument('email', type=str, required=True, help="email is required")
my_user_request.add_argument('password', type=str, required=True, help="password is required")
my_user_request.add_argument('photoUrl', type=str)

class User(Resource):

    def get(self, id):
        user = UserModel.find_user_by_id(id)
        if user: 
            return user.json()
        return {'message':'user not found'}, 200 # or 204

    def delete(self, user_id):
        user = UserModel.find_user_by_id(user_id)
        if user:
            user.delete_user()
            return {'message' : 'user deleted.'}
        return {'message' : 'user not founded'}, 204

    def post(self, id = 0):
        dados = my_user_request.parse_args()
        
        if UserModel.find_user_by_login(dados['login']):
            return {'message':'Login {} already exists'.format(dados['login'])}, 200

        id = UserModel.find_last_user()
        new_user = UserModel(id, **dados)
        
        try:
            new_user.save_user()
        except:
            return {'message':'An internal error ocurred.'}, 500

        return new_user.json(), 201

class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = my_login_request.parse_args()
        user = UserModel.find_user_by_login(dados['login'])
        if user and user.password == dados['password']:
            token_acesso = create_access_token(identity=user.user_id)
            return {
                'accessToken': token_acesso,
                'userId': user.user_id
            }, 200
        return {'message': 'User or password is not correct.'}