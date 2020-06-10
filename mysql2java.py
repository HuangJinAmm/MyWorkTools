import pymysql

url = "jdbc:mysql://192.168.0.250:3306/plat"
usr = "plat"
pswd = "plat%123"

def do():
    mysql_conn = pymysql.connect(host= '192.168.0.250', port= 3306, user= usr, password= pswd, db= 'plat')
    sql = '''SELECT 
    COLUMN_NAME , 
    COLUMN_TYPE , 
    DATA_TYPE , 
    CHARACTER_MAXIMUM_LENGTH , 
    IS_NULLABLE , 
    COLUMN_DEFAULT , 
    COLUMN_COMMENT ,
FROM
 INFORMATION_SCHEMA.COLUMNS
where
-- developerclub为数据库名称，到时候只需要修改成你要导出表结构的数据库即可
-- table_schema ='developerclub'
-- AND
-- article为表名，到时候换成你要导出的表的名称
-- 如果不写的话，默认会查询出所有表中的数据，这样可能就分不清到底哪些字段是哪张表中的了，所以还是建议写上要导出的名名称
table_name  = 'tc_company_info'
'''
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