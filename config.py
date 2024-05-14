

#class Config:
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/FinalTestISA'
    #SQLALCHEMY_TRACK_MODIFICATIONS = False

# config.py

import os

class Config:
    SECRET_KEY = '$$TN2R$$'  # Consider using os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://Pinkode:Rn2T2021@myserverdb1.mysql.database.azure.com/badelha1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    
    
   