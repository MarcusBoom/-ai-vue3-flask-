from flask import Flask
from .exts import init_exts
from .urls import *
import config
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)


class My_filter(logging.Filter):
    def __init__(self, name):
        self.name = name

    def filter(self, record: logging.LogRecord) -> bool:
        return True


def create_app():
    # 连接数据库
    # app.config["SQLALCHEMY_DATABASE_URI"] = ""
    app.config.from_object(config)
    init_exts(app)

    return app


# 日志
def init_logfile():
    logging.basicConfig(level=logging.WARNING)
    # 记录位置
    handler = RotatingFileHandler(filename='logs/log', maxBytes=1024*1024*10, backupCount=10, encoding='utf-8')
    # 记录格式
    my_format = logging.Formatter("%(levelname)s %(filename)s :%(lineno)s %(message)s")
    handler.setFormatter(my_format)
    filter = My_filter("dev")
    handler.addFilter(filter)
    logger = logging.getLogger()
    logger.handlers.append(handler)





