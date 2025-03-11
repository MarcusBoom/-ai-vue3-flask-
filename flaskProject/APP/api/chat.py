from flask import request, jsonify
from flask_restful import Resource
from APP.api import glm4_api
from APP.api import SparkApi
from flask_jwt_extended import jwt_required, get_jwt_identity
from APP.models import *

appid = "fd8f5981"
api_secret = "OWE5NjRiZTY0YTRkOThjN2M3Y2VjZjdi"
api_key = "d0154245398b14492c3a56e2d4eba134"

#用于配置大模型版本，默认“general/generalv2”
domain = "general"   # v1.5版本
# domain = "generalv2"    # v2.0版本

#云端环境的服务地址
Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
# Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址


text = []

# length = 0


def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text


class Chat(Resource):
    def __init__(self):
        self.role = ""

    def post(self):
        user_input = request.json
        print(user_input)

        self.role = user_input["role"]
        if (user_input["model"] == "xinghuo"):
            question = checklen(getText("user", user_input['userInput']))
            SparkApi.answer = ""
            SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
            model_response = "Chat answers: " + SparkApi.answer
            return jsonify({'code': 200, 'answer': model_response})
        elif (user_input["model"] == "glm-4"):

            model_response = glm4_api.main(user_input['userInput'], self.role, "glm-4")
            model_response = "Chat answers: " + model_response
            return jsonify({'code': 200, 'answer': model_response})
        else:
            model_response = glm4_api.main(user_input['userInput'], self.role,"glm-4-0520")
            model_response = "Chat answers: " + model_response
            return jsonify({'code': 200, 'answer': model_response})

    def get(self):
        # print("请求接受")
        sessions = ChatModelsModel.query.with_entities(ChatModelsModel.name).all()
        # print(sessions)
        # sessions = ChatModelsModel.query.filter_by(ChatModelsModel.name).all()
        model_name = [session[0] for session in sessions]
        sessions = ListRoles.query.with_entities(ListRoles.role).all()
        role_name = [session[0] for session in sessions]
        # print(model_name)
        return {'code': 200, 'model_name': model_name, 'role_name':role_name}
