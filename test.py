import pymysql

my_db = pymysql.connect(
    host="myserverdb1.mysql.database.azure.com",
    port=3306,
    user="Pinkode",
    password="Rn2T2021",
    database="badelha1"
) 

my_cursor = my_db.cursor()


for db in my_cursor:
    print(db)