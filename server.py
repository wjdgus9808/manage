from flask import Flask, request,render_template
from datetime import datetime
from order import getOrderList, getOrder, setOrder
from volvo import getvList,upload,make_order,getVorderList
import pymysql
import pandas as pd
import numpy as np

app = Flask(__name__)

def template(content,list=None):
    return f'''<!doctype html>
    <html>
        <link rel="stylesheet" href="./static/css/style.css">
        <div class="navbar">
            <h1><a href="/">Prin Tech</a></h1>
            <ul class="nav_menu">
                <li><a href="/ord_make">생산입력</a></li>
                <li><a href="/ord_mnge">생산관리</a></li>
                <li><a href="/ord_plan">생산계획</a></li>
            </ul>
        </div>
        {content}
    </html>
    '''
 
@app.route('/')
def index():
    return template('<h2>안녕하세요</h2>')


@app.route('/ord_make')
def ord_make(): 
    content='''
    <h2>생산입력</h2>
    <form action="/ord_make_list" method="POST">
            <p>
                <input type="date" name="po_date"/>
                <input type="submit" value="조회"/>
            </p>
        </form>  
  
    '''
    return template(content)

@app.route('/ord_make_list',methods=['POST'])
def ord_make_list():
    po_date = request.form["po_date"].replace('-','')
    print(po_date)
    vlist = getvList(request.form["po_date"].replace('-',''))
    vordlist = getVorderList(request.form["po_date"].replace('-',''))
    return render_template('volvo.html',vlist=vlist,vordlist=vordlist,po_date=po_date)

@app.route('/ord_upload/<po_date>', methods=["POST"])
def ord_upload(po_date):
    if request.method == 'POST': 
        print(request.files['file'])
        f = request.files['file']
        data = pd.read_excel(f)
        data = data.replace({np.nan:None})
        for idx in range(len(data)):
            data['f_id'] = "test"    
            data['l_id'] = "test"   
            data['prsc_yn'] = 'N'
            data['po_date'] = po_date
            # data['po_date'] = data['Order date']         
        # print(data.loc[0]['Order date'])
        upload(po_date,data)
        
        vlist = getvList(po_date)   
        make_order(po_date,"yyyy") 
        vordlist = getVorderList(request.form["po_date"].replace('-',''))
        return render_template('volvo.html',vlist=vlist,vordlist=vordlist,po_date=po_date)





g_gubn = ''
g_fr_date = ''
g_to_date = ''
@app.route('/ord_mnge', methods=['GET'])
def ord_mnge():
    global g_gubn,g_fr_date,g_to_date    
    if( g_gubn == ''):
        g_gubn = '주문일자'
    if( g_fr_date == ''):
        g_fr_date = datetime.today().strftime('%Y%m%d')    
    if( g_to_date == ''):
        g_to_date = datetime.today().strftime('%Y%m%d')
    
    list = getOrderList(g_gubn, g_fr_date,g_to_date)
    return render_template('order_list.html',list = list, p_gubn=g_gubn, p_fr_date=g_fr_date, p_to_date=g_to_date)

@app.route('/ord_mnge_list/', methods=['POST'])
def ord_mnge_list():  
    global g_gubn,g_fr_date,g_to_date       
    g_gubn = request.form.get('gubn', False) 
    g_fr_date = request.form["fr_date"]
    g_to_date = request.form["to_date"]  
    list = getOrderList(g_gubn, g_fr_date,g_to_date)
    return render_template('order_list.html', list = list, p_gubn=g_gubn, p_fr_date=g_fr_date, p_to_date=g_to_date)

@app.route('/ord_mnge_detl/<string:seq>/', methods=['GET'])
def ord_mnge_detl(seq):      
    list = getOrder(seq)    
    return render_template('order_detl.html', list = list)
    
@app.route('/ord_mnge_upd/', methods=['POST'])
def ord_mnge_upd():      
    seq = request.form.get('seq')
    delv_chng_date = request.form['delv_chng_date']    
    val = setOrder(seq,delv_chng_date)    
    list = getOrder(seq)
    return render_template('order_detl.html',list=list)
    










@app.route('/ord_plan')
def ord_plan():
    return template('<h2>생산계획</h2>')
    

















if __name__ == '__main__':
    app.run(port='5000' ,debug=True)