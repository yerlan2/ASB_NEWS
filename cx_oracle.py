import cx_Oracle


try:
    conn = cx_Oracle.connect('ora_proj2/hr@//localhost:1521/XE')
except Exception as err:
    print('Error while creating the connection ', err)
else:
    try:
        cur = conn.cursor()
        sql_select = """
            SELECT * FROM USERS
            """
        cur.execute(sql_select)
        row = cur.fetchall()
        for i, record in enumerate(row):
            print(f"{i:3} : {record}")
    except Exception as err:
        print('Exception occured while fetching the records ', err)
    else:
        print('Query Completed.')
    finally:
        cur.close()
finally:
    conn.close()


