from flask_restful import Resource, marshal_with, fields, reqparse
from werkzeug.security import check_password_hash,generate_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)
from flask import request
from APP.models import *

class Login(Resource):
    def post(self):
        try:
            form_data = request.json
            username = form_data['username']
            password = form_data['password']
            user = Users.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)
                return {
                    "msg": "登录成功",
                    "code": 200,
                    "data": {"user_id": user.id,
                    "access_token": access_token,
                    "refresh_token": refresh_token}
                }
            else:
                return {"msg": "登录失败", "code": 401}, 401
        except Exception as e:
            print(f"发生错误: {e}")
            return {"msg": "内部服务器错误", "code": 500}


class Register(Resource):
    def post(self):
        try:
            json_data = request.json
            print(json_data)
            username = json_data['username']
            user = Users.query.filter_by(username=username).first()
            if user:
                return {"msg": "用户名重复", "code": 234}, 234
            hashed_password = generate_password_hash(json_data['password'])
            new_session = Users(
                username=username,
                password=hashed_password,
                name=json_data['name'],
                position=json_data['organization'],
                department_id = 0
            )
            db.session.add(new_session)
            db.session.commit()
            db.session.close()
            return {"msg": "注册成功", "code": 200}, 200
        except Exception as e:
            print(f"发生错误: {e}")
            return {"msg": "内部服务器错误", "code": 500}, 500


user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help="username is required")
user_parser.add_argument('name', type=str, required=False, help='Name of the user')
user_parser.add_argument('age', type=int, required=False, help='Age of the user')


class UserProfileResource(Resource):
    @jwt_required()
    def get(self):
        # 假设用户已登录，可以从当前用户的信息中获取用户ID或用户名
        current_user = get_jwt_identity()
        user = Users.query.filter_by(id=current_user).first()
        if user:
            user_profile = {
                'username': user.username,
                'name': user.name,
                'age': user.age,
                'role': user.admine
            }
            return {'code': 200, 'data': user_profile}, 200
        else:
            return {'message': 'User not found', 'code': 404}, 404


# 资源 - 更新用户个人信息
class UpdateUserProfileResource(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        args = user_parser.parse_args()
        user = Users.query.filter_by(id=current_user).first()
        if user:
            # 更新用户信息
            user.username = args['username'] if args['username'] else user.username
            user.name = args['name'] if args['name'] else user.name
            user.age = args['age'] if args['age'] else user.age
            db.session.commit()
            return {'code': 200, 'message': 'Profile updated successfully', 'data': {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'age': user.age
            }}
        else:
            return {'code': 404, 'message': 'User not found'}

    @jwt_required()
    def put(self):
        current_user = get_jwt_identity()
        new_password = request.json
        print(new_password)
        user = Users.query.filter_by(id=current_user).first()
        # hashed_password = generate_password_hash("123")
        if not check_password_hash(user.password, new_password['currentPassword']):
            return {'message': 'The original password is incorrect', 'code': 201}, 201
        else:
            hashed_password = generate_password_hash(new_password['newPassword'])
            user.password = hashed_password
            db.session.commit()
            db.session.close()
            return {'message': 'The password was successfully changed', 'code': 200}, 200


class RefreshTokenResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        refresh_token = create_access_token(identity=current_user)
        access_token = create_access_token(identity=current_user)
        return {'user_id': current_user, 'access_token': access_token, 'refresh_token': refresh_token}, 200
