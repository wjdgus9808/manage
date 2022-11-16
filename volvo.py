import pymysql
import pandas as pd
import numpy as np

def getvList(po_date):    
        
    gil_db = pymysql.connect(
        user='admin', 
        passwd='789456123', 
        host='database-1.cozswa2vem5d.ap-northeast-2.rds.amazonaws.com', 
        db='prin_tech', 
        charset='utf8'
    )
    cursor = gil_db.cursor()
    print("test: ",po_date)
    
    sql = f"""
            SELECT po_number,item,material_no,print_qty,material_desc,plant,sloc,net_price,order_date,order_qty,delivery_date,rcvd_qty,qc,location from volvo WHERE po_date = "{po_date}" 
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

def getVorderList(po_date):
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
                        b.type,
                        b.size,
                        a.ord_qty,
                        b.txtr,
                        b.prnt,
                        concat('MV-', substr(a.ord_date, 5,2) , '-' , po_mon_no)  ord_no,
                        a.delv_date,
                        b.price,
                        cast(b.price as unsigned)*cast(a.ord_qty as unsigned) tot_price,
                        b.page,
                        ifnull(a.delv_chng_date,a.delv_date) delv_chng_date
 
                    FROM vorder a
                    left outer join prdc_mst b on b.part_no = a.part_no
                    WHERE a.po_date = {po_date}
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
    print("order list: ",list)
    return list

def upload(po_date,data):
    gil_db = pymysql.connect(
        user='admin', 
        passwd='789456123', 
        host='database-1.cozswa2vem5d.ap-northeast-2.rds.amazonaws.com', 
        db='prin_tech', 
        charset='utf8'
        )
    cursor = gil_db.cursor()
    sql_insert = 'INSERT INTO prin_tech.volvo(po_number,item,material_no,print_qty,material_desc,plant,sloc,net_price,order_date,order_qty,delivery_date,rcvd_qty,qc,location,f_id,l_id,proc_yn,po_date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    for idx in range(len(data)):
        cursor.execute(sql_insert,tuple(data.values[idx]))
    gil_db.commit()
    gil_db.close()






def make_order(po_date,usid):
    gil_db = pymysql.connect(
        user='admin', 
        passwd='789456123', 
        host='database-1.cozswa2vem5d.ap-northeast-2.rds.amazonaws.com', 
        db='prin_tech', 
        charset='utf8'
    )
    cursor = gil_db.cursor()
    cursor.callproc('make_order',(po_date,usid))
    gil_db.commit()
    gil_db.close()

