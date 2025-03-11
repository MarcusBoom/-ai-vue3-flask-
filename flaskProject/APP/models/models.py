from ..exts import db
# from werkzeug.security import  check_password_hash
from flask_restful import Resource


# 会话列表


class ChatItemsModel(db.Model):
    __tablename__ = 'chat_items'
    chat_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    userid = db.Column(db.Integer, nullable=False)
    model_id = db.Column(db.Integer)
    title = db.Column(db.String(100), nullable=False)


class ChatHistoryModel(db.Model):
    __tablename__ = 'chat_history'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    chat_id = db.Column(db.Integer, nullable=False)
    userid = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50))
    content = db.Column(db.UnicodeText)
    # tokens = db.Column(db.Integer, default=0)
    # use_context = db.Column(db.Boolean, default=1)
    created_at = db.Column(db.String(100))
    updated_at = db.Column(db.String(100))


# 模型表
class ChatModelsModel(db.Model):
    __tablename__ = 'chat_models'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    platform = db.Column(db.String(40))  # 模型平台
    name = db.Column(db.String(50))  # 模型名称
    value = db.Column(db.String(50))  # 模型值
    enabled = db.Column(db.Boolean, default=1)
    url = db.Column(db.String(100))


# 图片识别
class TextImgModel(db.Model):
    __tablename__ = 'text_img'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.String(50))
    name = db.Column(db.String(100))
    content = db.Column(db.UnicodeText)
    use_context = db.Column(db.Boolean, default=1)
    created_at = db.Column(db.String(100))


# appid
class ApiKeyModel(db.Model):
    __tablename__ = 'api_key'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    platform = db.Column(db.String(40))  # 模型平台
    value = db.Column(db.String(100))  # key值 appid|appkey|apisecret
    # 模型的资源序列化函数（方法）
    # 在该函数中所返回的dict的keys，将是我们从test表里所序列化的字段

    def schema(self):
        return {
            'id': self.id,
            'platform': self.platform,
            'value': self.value
        }


class ListRoles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String())
    content = db.Column(db.UnicodeText)


class Department(db.Model):
    __tablename__ = 'department'
    department = db.Column(db.String())
    parent_id = db.Column(db.Integer)
    created_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    department_pinyin = db.Column(db.String())
    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)


# class Department_user(db.Model):
#     __tablename__ = 'department_user'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String())
#     age = db.Column(db.Integer)
#     email = db.Column(db.String(255))
#     phone = db.Column(db.String(20))
#     department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'))