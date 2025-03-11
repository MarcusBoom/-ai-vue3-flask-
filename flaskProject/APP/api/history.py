from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify
from APP.models import *
from datetime import datetime


class Chat_History(Resource):
    @jwt_required()
    def get(self, chat_id):
        chat_history = ChatHistoryModel.query.filter_by(chat_id=chat_id).all()

        # 将聊天历史记录转换为字典列表
        chat_history_dict = [
            {
                'chat_id': record.chat_id,
                'userid': record.userid,
                'type': record.type,
                'content': record.content,
                'created_at': record.created_at,
                'updated_at': record.updated_at
            }
            for record in chat_history
        ]

        return jsonify({'chatHistory': chat_history_dict})

    @jwt_required()
    def post(self, chat_id):
        data = request.json
        current_user = get_jwt_identity()
        # 创建新的聊天历史记录
        new_chat_history = ChatHistoryModel(
            chat_id=chat_id,
            userid=current_user,
            type=data['type'],
            content=data['content'],
            created_at=str(datetime.utcnow()),
            updated_at=str(datetime.utcnow())
        )

        db.session.add(new_chat_history)
        db.session.commit()

        return jsonify({'message': 'Chat history saved successfully'})

    @jwt_required()
    def delete(self, chat_id):
        ChatItemsModel.query.filter_by(chat_id=chat_id).delete()
        ChatHistoryModel.query.filter_by(chat_id=chat_id).delete()
        db.session.commit()
        return jsonify({'code':200})
