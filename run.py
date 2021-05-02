import etcd3
import json
import os
from fastapi import FastAPI
etcd_ip = os.environ.get('ETCD_IP_ADDR')
etcd_port =os.environ.get('ETCD_PORT')
# etcd = etcd3.client(host=os.environ.get('ETCD_IP_ADDR'), port=int(os.environ.get('ETCD_PORT')))
def get_data_from_etcd():
    etcd = etcd3.client(host='127.0.0.1', port=2379)
    json_dic ={}
    for value, metadata in etcd.get_all():
        json_dic.update({metadata.key.decode('utf-8'):value.decode('utf-8')})
    return json.dumps(json_dic)

app = FastAPI()
@app.get('/')
async def send_data():
    return get_data_from_etcd(get_data_from_etcd())



