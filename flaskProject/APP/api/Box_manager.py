from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from APP.models import *


# 左侧接口
class UserClass(Resource):

    @jwt_required()
    def post(self):
        form_session = request.json
        current_user = get_jwt_identity()
        new_session = ChatItemsModel(
        model_id=3,
        userid=current_user,
        title = form_session.get('name'),
        )
        db.session.add(new_session)
        db.session.commit()
        db.session.close()
        return {"msg":"创建成功","code":200,"chat_id":current_user}

    @jwt_required()
    def get(self):
        # print("请求接受")
        current_user = get_jwt_identity()
        sessions = ChatItemsModel.query.filter_by(userid=current_user).all()
        # print(sessions)
        session = [{
            'id': session.chat_id,
            'name': session.title,
            'userInput': '',
            'chatGPTAnswer': '',
            'messageHistory': []
        } for session in sessions]
        return {'code': 200, 'chatBoxes': session}

    @jwt_required()
    def delete(self):
        form_seesion = request.json
        chat_id = form_seesion.get('chat_id')
        session = ChatItemsModel.query.filter_by(chat_id=chat_id).first()
        if not session:
            return {"msg":"会话不存在","code":400}
        db.session.delete(session)
        db.session.commit()
        return {"msg":"删除成功","code":200}

# 改名字
    @jwt_required()
    def put(self):
        form_session = request.json
        chat_id = form_session.get('boxId')
        title = form_session.get('newName')
        session = ChatItemsModel.query.filter_by(chat_id=chat_id).first()
        print(session)
        if not session:
            return {"msg":"会话不存在","code":400}
        session.title = title
        db.session.commit()
        return {"msg":"修改成功","code":200}










