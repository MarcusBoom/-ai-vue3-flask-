from ..exts import db
import json


class Users(db.Model):
    __tablename__ = "Users"
    # 指定变量类型
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    name = db.Column(db.String(40))
    password = db.Column(db.String(200))
    age = db.Column(db.Integer)
    position = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    admine = db.Column(db.Boolean, default=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'))

# 方法
    def __repr__(self):
        return json.dumps({"username": self.username})
