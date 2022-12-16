import pymysql.cursors
# Connect to the database
CONNECTION = pymysql.connect(host='localhost',
                             user='root',
                             password='Bolero2000@',
                             db='cotonwatedb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)