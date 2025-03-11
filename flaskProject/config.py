# 数据库
from datetime import timedelta

DB_DATABASE_NAME = "postgresql"
DB_DRIVER = "psycopg2"
DB_USERNAME = "postgres"
DB_PASSWORD = "123456"
DB_NAME = "flask"
DB_HOST = "localhost"
DB_PORT = 5432

# pgSQL+DRIVER://username:password@host:port/name
SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(DB_DATABASE_NAME, DB_USERNAME, DB_PASSWORD,
                                                         DB_HOST, DB_PORT, DB_NAME)


# JWT
JWT_SECRET_KEY = "123456"
JWT_ACCESS_TOKEN_EXPIRE = timedelta(hours=5)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=24)
