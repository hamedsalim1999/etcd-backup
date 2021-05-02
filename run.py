import etcd3
import json
import os
from fastapi import FastAPI
etcd_ip = os.environ.get('ETCD_IP_ADDR')
etcd_port =os.environ.get('ETCD_PORT')
def get_data_from_etcd(etcd_port, etcd_ip):
    etcd = etcd3.client(etcd_port, etcd_ip)
    json_dic ={}
    for value, metadata in etcd.get_all():
        json_dic.update({metadata.key.decode('utf-8'):value.decode('utf-8')})
    return json.dumps(json_dic)

app = FastAPI()
@app.get('/')
async def send_data():
    return get_data_from_etcd(etcd_ip,etcd_port)



