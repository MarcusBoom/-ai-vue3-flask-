import json  # 导入处理 JSON 数据的模块
import pandas as pd  # 导入数据处理库 pandas
from zhipuai import ZhipuAI  # 导入 ZhipuAI 类，用于与智能聊天模型交互
from APP.api import functionsList as fun  # 导入函数列表（假设是一个模块）
import pprint
# 创建 ZhipuAI 客户端实例，传入 API 密钥
client_zhipu = ZhipuAI(api_key="9b503b7a3f465be7d8e6ed690d5d819f.TvRhA2V4PVHKcT3q")

# 定义一个聊天会话类 ChatConversation
class ChatConversation:
    def __init__(self):
        self.model = ""  # 设置模型名称
        self.messages = []  # 初始化消息列表为空
        self.function_repository = {}  # 初始化函数仓库为空字典
        self.saved_info = {}  # 初始化保存信息的字典

    def function(self):
        # 返回一个包含两个函数描述的列表
        return [{
            "type": "function",
            "function": {
                "name": "calculate_total_age_function",  # 函数名
                "description": "从按'split'方向排列的JSON字符串中计算总年龄。",  # 函数描述
                "parameters": {
                    "type": "object",
                    "properties": {
                        "input_json": {
                            "description": "以split方向组织的JSON字符串，其中包含用于计算年龄总和的数据。",
                            "type": "string"
                        }
                    },
                    "required": ["input_json"]
                },
                "returns": {
                    "description": "返回一个包含总年龄的JSON字符串，格式为{\"total_age\": \"<sum_of_ages>\"}。",
                    "type": "string"
                }
            }
        }, {
            "type": "function",
            "function": {
                "name": "calculate_married_count_function",  # 函数名
                "description": "从按'split'方向排列的JSON字符串中计算已婚个体的数量。",  # 函数描述
                "parameters": {
                    "type": "object",
                    "properties": {
                        "input_json": {
                            "description": "包含个体婚姻状况的JSON字符串，格式为'split'。",
                            "type": "string"
                        }
                    },
                    "required": ["input_json"]
                },
                "returns": {
                    "description": "返回一个包含已婚个体数量的JSON字符串，格式为{\"married_count\": \"<count>\"}。",
                    "type": "string"
                }
            }
        }, {
            "type": "function",
            "function": {
                "name": "send_email",
                "description": "使用QQ邮箱向指定的收件人发送邮件。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sender_email": {
                            "description": "发件人的QQ邮箱地址。",
                            "type": "string"
                        },
                        "sender_pass": {
                            "description": "发件人的QQ邮箱授权码。",
                            "type": "string"
                        },
                        "recipient_email": {
                            "description": "收件人的邮箱地址。",
                            "type": "string"
                        },
                        "subject": {
                            "description": "邮件主题。",
                            "type": "string"
                        },
                        "body": {
                            "description": "邮件正文。",
                            "type": "string"
                        }
                    },
                    "required": ["sender_email", "sender_pass", "recipient_email", "subject", "body"]
                },
                "returns": {
                    "description": "邮件发送的结果信息。",
                    "type": "string"
                }
            }
        }, {
            "type": "function",
            "function": {
                "name": "fetch_last_email",
                "description": "查询指定用户的QQ邮箱中最后一封邮件信息。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_email": {
                            "description": "需要查询的QQ邮箱的用户邮箱。",
                            "type": "string"
                        },
                        "user_pass": {
                            "description": "需要查询的QQ邮箱的用户码。",
                            "type": "string"
                        }
                    },
                    "required": ["user_email", "user_pass"]
                },
                "returns": {
                    "description": "包含最后一封邮件全部信息的JSON格式字符串。如果查询失败，返回包含错误信息的JSON格式字符串。",
                    "type": "string"
                }
            }
        }]

    def add_function(self, functions_list):
        # 将传入的函数列表转换为以函数名为键，函数对象为值的字典存储在函数仓库中
        self.function_repository = {func.__name__: func for func in functions_list}

    def _call_chat_model(self, functions=None, include_functions=False):
        # 定义调用聊天模型的内部方法，接受函数描述列表和是否包含函数描述的标志
        params = {
            "model": self.model,  # 使用指定的模型名称
            "messages": self.messages,  # 使用当前存储的消息列表
            "top_p": 0.7,  # 设置聊天模型的 top_p 参数
            "temperature": 0.9,  # 设置聊天模型的 temperature 参数
            "stream": False,  # 禁用流式处理
            "max_tokens": 2000,  # 设置最大生成 token 数量
        }

        if include_functions:
            params["tools"] = functions  # 如果需要包含函数描述，将函数描述列表作为参数传入
        try:
            return client_zhipu.chat.completions.create(**params)  # 调用 ZhipuAI 客户端的聊天模型接口
        except Exception as e:
            print(f"Error calling chat model: {e}")  # 捕获异常并打印错误信息
            return None  # 返回 None 表示调用失败

    def run(self, functions_list=None):
        try:
            if functions_list is None:
                response = self._call_chat_model()  # 如果未传入函数列表，则直接调用聊天模型
                if response is None:
                    return "Error: No response from chat model."
                final_response = response.choices[0].message.content  # 获取并返回模型的第一个响应内容
                return final_response
            else:
                self.add_function(functions_list)  # 如果传入了函数列表，则将其添加到函数仓库中
                functions = self.function()  # 生成每个函数的 JSON Schema 描述
                response = self._call_chat_model(functions, include_functions=True)  # 调用聊天模型，包含函数描述
                if response is None:
                    return "Error: No response from chat model."
                print(response)
                response_message = response.choices[0].message  # 获取响应消息对象
                # print(f"Response message: {response_message}")
                if response_message.tool_calls is not None:  # 如果存在工具调用
                    function_name = response_message.tool_calls[0].function.name  # 获取调用的函数名
                    function_call_exist = self.function_repository.get(function_name)  # 获取函数仓库中的函数对象

                    if not function_call_exist:
                        print(f"Function {function_name} not found in functions repository.")  # 如果函数不存在，则打印错误信息
                        return None
                    # print(response_message.tool_calls[0].function.arguments)
                    function_args = json.loads(response_message.tool_calls[0].function.arguments)  # 解析函数调用的参数
                    self.saved_info.update(function_args)  # 更新已保存的信息
                    # print(function_args)
                    # 检查是否有缺失的信息
                    missing_info = [key for key, value in function_args.items() if not value]
                    print(f"缺失值 {missing_info}")
                    if missing_info:
                        # 请求用户补全缺失的信息
                        missing_info_prompt = "请补全以下缺失的信息: " + ", ".join(missing_info)
                        self.messages.append({"role": "user", "content": missing_info_prompt})
                        return missing_info_prompt

                    function_response = function_call_exist(**self.saved_info)  # 调用函数并获取返回值
                    self.messages.append(response_message.model_dump())  # 将响应消息转换为字典并追加到消息列表中
                    self.messages.append({  # 将函数调用的返回值追加到消息列表中
                        "content": function_response,
                        "role": "tool",
                        "tool_call_id": response_message.tool_calls[0].id
                    })
                    second_response = self._call_chat_model(functions=functions, include_functions=True)  # 再次调用聊天模型
                    if second_response is None:
                        return "Error: No response from chat model."
                    final_response = second_response.choices[0].message.content  # 获取第二次调用的响应内容
                    return final_response
                else:
                    return response_message.content
        except Exception as e:
            print(f"An error occurred: {e}")  # 捕获异常并打印错误信息
            return None  # 返回 None 表示出现错误

# 主函数入口
def main(question, role, model_name):
    df_complex = pd.DataFrame({  # 创建一个包含复杂数据的 DataFrame
        'Name': ['张三', '李四', '王五'],
        'Age': [25, 30, 35],
        'Salary': [50000.0, 100000.5, 150000.75],
        'IsMarried': [True, False, True]
    })

    messages = [{"role": "user", "content": "%s" % question}]

    # 初始化 ChatConversation 实例
    chat = ChatConversation()
    chat.model = model_name
    # 将消息添加到聊天记录中
    chat.messages = messages

    functions_list = [fun.calculate_total_age_function, fun.calculate_married_count_function, fun.fetch_last_email, fun.send_email]  # 外部函数列表
    if role == "Data Analyst":
        chat.messages.append({"role": "system",
                              "content": "你是一位优秀的数据分析师，现在有这样一份通讯录信息：'%s'。不要假设或猜测传入函数的参数值。如果用户的描述不明确，请要求用户提供必要信息" % df_complex.to_json(orient='split')})
        response = chat.run(functions_list=functions_list)
    elif role == "User":
        response = chat.run()
    elif role == "mail":
        sender_email = '1916983913@qq.com'
        sender_pass = 'xzuycseoijakcffa'
        chat.messages.append({"role": "system", "content": "你是一位优秀的邮件处理员，不要假设或猜测传入函数的参数值，没有提及的参数不要猜测传入值。如果用户的描述不明确，请要求用户提供必要信息，如果要发送邮件或者查看邮件这是用户的邮件的邮箱账号和授权码: '%s', '%s'" % (
                sender_email, sender_pass)})
        response = chat.run(functions_list=functions_list)
    return response  # 返回响应内容

# 示例调用 main 函数
# question = "发送信息给466227473@qq.com,标题：114514，内容：111111"
# role = "mail"
# response = main(question, role)
# print(response)
