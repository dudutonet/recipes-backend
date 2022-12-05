from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS

from resources.recipes import Recipe, Recipes
from resources.users import User, UserLogin

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})

# conexão com mysql
DATABASE_URI = 'mysql+pymysql://root@localhost/recipes?charset=utf8mb4'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'

#conexão com postgres
# DATABASE_URI = 'postgresql+psycopg2://postgres:admin@localhost:5432/dbpython'
# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'Senai2022'

@app.before_first_request
def create_database():
    database.create_all()

api.add_resource(Recipe, '/recipes/<int:id>')
api.add_resource(Recipes, '/recipes')
api.add_resource(User, '/users/<int:id>')
api.add_resource(UserLogin, '/login')


if __name__ == '__main__':
    from sql_alchemy import database
    database.init_app(app)
    app.run(debug=True)
