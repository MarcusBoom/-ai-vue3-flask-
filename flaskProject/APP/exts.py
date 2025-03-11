# 扩展初始化
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

api = Api()
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()


def init_exts(app):
    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    jwt.init_app(app)
