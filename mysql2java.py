import pymysql

url = "jdbc:mysql://192.168.0.250:3306/plat"
usr = "plat"
pswd = "plat%123"

def do():
    mysql_conn = pymysql.connect(host= '192.168.0.250', port= 3306, user= usr, password= pswd, db= 'plat')
    sql = "desc plat"
    ret = do_query(mysql_conn,sql)
    mysql_conn.close()

def do_query(conn,sql):
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            select_result = cursor.fetchall()
            for result_one in select_result:
                print(result_one)
    except Exception as e:
        print(e)
    return select_result

if __name__ == "__main__":
    do()