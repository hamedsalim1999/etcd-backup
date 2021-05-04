# from fastapi import FastAPI
from datetime import datetime
import etcd3
import json
import os
import sqlite3

etcd_ip = os.environ.get('ETCD_IP_ADDR')
etcd_port =os.environ.get('ETCD_PORT')

def backup_from_etcd(etcd_port, etcd_ip):
    datetime_name= datetime.now().strftime("%d. %B %Y %I:%M%p")
    etcd = etcd3.client(etcd_port, etcd_ip)
    con = sqlite3.connect(f'{datetime_name}.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS etcd (key TEXT, value TEXT)")
    json_dic ={}
    for val, metadata in etcd.get_all():
        json_dic.update({metadata.key.decode('utf-8'):val.decode('utf-8')})
        cur.execute("INSERT INTO etcd (key , value) VALUES (?, ?)",(metadata.key.decode('utf-8'),val.decode('utf-8')))
    with open(f'{datetime_name}.json', 'w') as json_file:
        json.dump(json_dic, json_file)

backup_from_etcd(etcd_port,etcd_ip)

# app = FastAPI()
# @app.get('/')
# async def send_data():
#     return get_data_from_etcd(etcd_ip,etcd_port)



