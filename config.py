import mysql.connector

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/FinalTestISA'
    SQLALCHEMY_TRACK_MODIFICATIONS = False