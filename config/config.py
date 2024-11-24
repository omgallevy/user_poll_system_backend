from pydantic import BaseSettings


class Config(BaseSettings):
    MYSQL_USER: str = 'user'
    MYSQL_PASSWORD: str = 'password'
    MYSQL_DATABASE: str = 'user_service'
    MYSQL_HOST: str = 'localhost'
    MYSQL_PORT: str = '3306'
    DATABASE_URL: str = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
    USER_ANSWER_SERVICE_BASE_URL = "http://localhost:8080/user_answers"
