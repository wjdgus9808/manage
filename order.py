# 불러오기
import pymysql
import pandas as pd
import numpy as np
 
def getOrderList(gubn, fr_date,to_date):    
        
    gil_db = pymysql.connect(
        user='admin', 
        passwd='789456123', 
        host='database-1.cozswa2vem5d.ap-northeast-2.rds.amazonaws.com', 
        db='prin_tech', 
        charset='utf8'
    )
    cursor = gil_db.cursor()
        
    
    sql = f"""
            SELECT 
                a.seq,
                a.part_no,
                b.part_hnm, 
                concat('MV-', substr(a.ord_date, 5,2) , '-' , po_mon_no)  ord_no,                
                a.ord_date,
                a.delv_date,
                a.delv_chng_date,
                a.po_date,
                b.type,
                b.size,
                a.ord_qty,
                b.txtr,
                b.prnt,                
                b.price,
                cast(b.price as unsigned)*cast(a.ord_qty as unsigned) tot_price,
                b.page,                                
                a.material_desc,
                a.net_price                                        
            FROM vorder a
            left outer join prdc_mst b on b.part_no = a.part_no
            WHERE case when '{gubn}' = 'A' then a.po_date else ifnull(a.delv_chng_date,a.delv_date) end between '{fr_date}' and '{to_date}'
            """

    print(sql)            

    cursor.execute(sql)    
    rows = cursor.fetchall()
        
    # price = []
    list = []
    for row in rows:
        # price.append(row[2])
        list.append(row)
    
    gil_db.close()
    return list





def getOrder(seq):    
        
    gil_db = pymysql.connect(
        user='admin', 
        passwd='789456123', 
        host='database-1.cozswa2vem5d.ap-northeast-2.rds.amazonaws.com', 
        db='prin_tech', 
        charset='utf8'
    )
    cursor = gil_db.cursor()

    sql = f"""
            SELECT a.part_no,
                b.part_hnm, 
                a.ord_date,                        
                a.delv_date,
                a.delv_chng_date,
                a.seq                        
            FROM vorder a
            left outer join prdc_mst b on b.part_no = a.part_no
            WHERE a.seq = {seq}
            """

    print(sql)        
    cursor.execute(sql)
    rows = cursor.fetchall()
        
    # price = []
    list = []
    for row in rows:
        # price.append(row[2])
        list.append(row)
    
    gil_db.close()
    return list

def setOrder(seq,delv_chng_date):    
        
    gil_db = pymysql.connect(
        user='admin', 
        passwd='789456123', 
        host='database-1.cozswa2vem5d.ap-northeast-2.rds.amazonaws.com', 
        db='prin_tech', 
        charset='utf8'
    )
    cursor = gil_db.cursor()

    sql = f"""
            UPDATE vorder
               SET delv_chng_date = {delv_chng_date}
                  ,l_id = '111'
                  ,l_dt = now()
             WHERE seq = {seq}
            """
    
    ret_val = cursor.execute(sql)
    gil_db.commit()
    gil_db.close()
        
    return ret_val