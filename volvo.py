import pymysql
import pandas as pd
import numpy as np

def getvList(order_date):    
        
    gil_db = pymysql.connect(
        user='admin', 
        passwd='789456123', 
        host='database-1.cozswa2vem5d.ap-northeast-2.rds.amazonaws.com', 
        db='prin_tech', 
        charset='utf8'
    )
    cursor = gil_db.cursor()
        
    
    sql = f"""
            SELECT * from volvo
                    WHERE order_date = {order_date} 
            """
    cursor.execute(sql)
    rows = cursor.fetchall()
        
    # price = []
    list = []
    for row in rows:
        # price.append(row[2])
        list.append(row)
    gil_db.close()
    return list