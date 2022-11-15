import pymysql

class Database():
    def __init__(self):
        self.db = pymysql.connect(
            host="database-1.cozswa2vem5d.ap-northeast-2.rds.amazonaws.com",
            user="admin",
            password="789456123",
            db="prin_tech",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor,
        )


    # def execute(self):
    #     ret = []
    #     curs = self.db.cursor()
    #     curs.execute("select * from prin_tech.volvo")
    #     rows = curs.fetchall()
    #     for e in rows:
    #         temp = {'empno':e['po_number'],'name':e['item'],'department':e['material_no'],'phone':e['print_qty'] }
    #         ret.append(temp)
        
    #     self.db.commit()
    #     self.db.close()
    #     return ret
        
    # def executeOne(self, query, args={}):
    #     self.cursor.execute(query, args)
    #     row = self.cursor.fetchone()
    #     return row
 
    # def executeAll(self, query, args={}):
    #     self.cursor.execute(query, args)
    #     row = self.cursor.fetchall()
    #     return row
 
    # def commit():
    #     self.db.commit()