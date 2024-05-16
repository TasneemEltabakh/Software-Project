import pymysql

my_db = pymysql.connect(
    host="myserverdb1.mysql.database.azure.com",
    port=3306,
    user="Pinkode",
    password="Rn2T2021",
    database="badelha1"
) 

my_cursor = my_db.cursor()



#my_cursor.execute("INSERT INTO promo_code (code, discount_percentage) VALUES ('zewail', 50)")
#my_cursor.execute("INSERT INTO category (`id`, `name`) VALUES ('2','men')")
#my_cursor.execute("INSERT INTO category (`id`, `name`) VALUES ('3','kid')")

#my_cursor.execute("SHOW TABLES")
#my_cursor.execute("CREATE DATABASE BADELHA1")
#my_cursor.execute("Select * from promocode")



for db in my_cursor:
    print(db)