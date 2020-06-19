import pymysql

url = "jdbc:mysql://192.168.0.250:3306/plat"
usr = "plat"
pswd = "plat%123"

def do():
    mysql_conn = pymysql.connect(host= '192.168.0.250', port= 3306, user= usr, password= pswd, db= 'plat')
    sql = "SELECT\
    COLUMN_NAME ,\
    COLUMN_TYPE ,\
    DATA_TYPE ,\
    CHARACTER_MAXIMUM_LENGTH ,\
    IS_NULLABLE ,\
    COLUMN_DEFAULT ,\
    COLUMN_COMMENT \
FROM INFORMATION_SCHEMA.COLUMNS where table_name  = 'tc_company_info'"
    # tabel_sql = "select table_name from information_schema.tables where table_schema='plat'"
    ret = do_query(mysql_conn,sql)
    # retable = do_query(mysql_conn,tabel_sql)
    slasdf asdfad asdfad

def do_query(conn,sql):
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            select_result = cursor.fetchall()
            for result_one in select_result:
                for r in result_one:
                    if isinstance(r,str):
                        print(r.encode("GBK"))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    do()