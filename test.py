import pymysql

my_db = pymysql.connect(
    host="myserverdb1.mysql.database.azure.com",
    port=3306,
    user="Pinkode",
    password="Rn2T2021",
    database="badelha1"
) 

my_cursor = my_db.cursor()



#my_cursor.execute("select * from user")
#my_cursor.execute("SHOW DATABASES")
#my_cursor.execute("CREATE DATABASE BADELHA1")
# my_cursor.execute("Select * from ")



for db in my_cursor:
    print(db)