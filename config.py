import mysql.connector

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/test3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False