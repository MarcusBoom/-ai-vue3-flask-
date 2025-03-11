# from flask import Flask, request, make_response, render_template
#
# app = Flask(__name__)
#
#
#
# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'
#
#
# def methed():
#     return "something"
#
#
# app.add_url_rule('/get/methed', view_func=methed)
#
#
# @app.route('/get/<any(abc,def):str>/', methods=['GET', 'POST'])
# def get_id(str):
#     print(str)
#     return "path is %s" % str
#
#
# @app.route('/request/', methods=['GET', 'POST'])
# def request_ussage():
#     # this_arg = request.args # 返回值为类字典型
#     # key1 = request.args.get("key1") # 在字典中获得变量
#     # print(type(key1), key1)
#     # data1 = request.get_data(as_text=True)
#     # print(type(data1),data1)
#     # data_json = json.dumps(this_arg)
#     json_data = request.json()
#     # header_type = request.headers.get('Content-Type')
#     # print(header_type)
#     print(type(json_data), json_data)
#     return "done"
#
#
# @app.route('/response/', methods=['GET', 'POST'])
# def response_ussage():
#     # 返回字符串
#     # res = make_response("get", 401)
#     res = make_response({"use": "used"}, 201)
#     # 返回模板
#     # res = make_response(render_template("index.html",name="zhangsan"), 200)
#
#     return res
from urllib import request

from APP import create_app


app = create_app()

# 不使用restful
# @app.route('/delete/<int: useid>')
# def method():
#     if request.method == 'GET':
#
#     elif request.method == 'POST':

# 使用restful,APP/api

if __name__ == '__main__':
    app.run(debug=True)
