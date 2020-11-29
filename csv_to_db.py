import pandas as pd
import numpy as np

data = pd.read_csv('news_with_labels_cleaned.csv')
del data['Unnamed: 0']
data = data.replace(np.nan, '')

import cx_Oracle

try:
    conn = cx_Oracle.connect('ora_proj2/hr@//localhost:1521/XE')
except Exception as err:
    print('Error while creating the connection ', err)
else:
    try:
        cur = conn.cursor()
        sql_insert_next = "INSERT INTO SOURCES(id, name) VALUES(SOURCES_SEQ.nextval, :1)"
        sql_insert_curr = "INSERT INTO SOURCES(id, name) VALUES(SOURCES_SEQ.currval, :1)"
        sql_insert = sql_insert_next
        for r in data['source.name']:
            try:
                cur.execute(sql_insert, [r])
                sql_insert = sql_insert_next
            except cx_Oracle.IntegrityError as e:
                errorObj, = e.args
                if errorObj.code == 1:
                    sql_insert = sql_insert_curr
                    continue
        
        cur = conn.cursor()
        sql_insert_next = "INSERT INTO CATEGORIES(id, name) VALUES(CATEGORIES_SEQ.nextval, :1)"
        sql_insert_curr = "INSERT INTO CATEGORIES(id, name) VALUES(CATEGORIES_SEQ.currval, :1)"
        sql_insert = sql_insert_next
        for r in data['category']:
            try:
                cur.execute(sql_insert, [r])
                sql_insert = sql_insert_next
            except cx_Oracle.IntegrityError as e:
                errorObj, = e.args
                if errorObj.code == 1:
                    sql_insert = sql_insert_curr
                    continue
    
        for x in data.values:
            try:
                cur = conn.cursor()
                sql_select = "SELECT id FROM sources WHERE name=:1"
                cur.execute(sql_select, [x[7]])
                temp_source_id = cur.fetchall()
                temp_source_id = temp_source_id[0][0]
            except Exception as ex: 
                print("Error1 !!! ", ex)

            try:
                cur = conn.cursor()
                sql_select = "SELECT id FROM categories WHERE name=:1"
                cur.execute(sql_select, [x[8]])
                temp_category_id = cur.fetchall()
                temp_category_id = temp_category_id[0][0]
            except Exception as ex: 
                print("Error2 !!! ", ex)
                
            try:
                cur = conn.cursor()
                sql_insert = "INSERT INTO ARTICLES VALUES(ARTICLES_SEQ.nextval, :1, :2, :3, :4, :5, :6, :7, TO_DATE(:8, 'YYYY-MM-DD\"T\"HH24:MI:SS\"Z\"') , :9)"
                data = (temp_source_id, temp_category_id, x[0], x[1], x[2], x[3], x[4], x[5], x[6])
                cur.execute(sql_insert, data)
            except Exception as ex: 
                print("Error3 !!! ", ex)
    except cx_Oracle.IntegrityError as e:
        errorObj, = e.args
        print('ERROR while inserting the data ', errorObj)
    else:
        print('Insert Completed.')
        conn.commit()
    finally:
        cur.close()
finally:
    conn.close()



