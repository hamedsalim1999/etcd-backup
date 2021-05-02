import etcd3
import json
import os
etcd_ip = os.environ.get('ETCD_IP_ADDR')
etcd_port =int(os.environ.get('ETCD_PORT')
etcd = etcd3.client(host=os.environ.get('ETCD_IP_ADDR'), port=int(os.environ.get('ETCD_PORT')))
def get_data_from_etcd(etcd_ip,etcd_port):
    etcd = etcd3.client(host=etcd_ip, port=etcd_port)
    json_dic ={}
    for value, metadata in etcd.get_all():
        json_dic.update({metadata.key.decode('utf-8'):value.decode('utf-8')})
    return json_object=json.dumps(json_dic)

print(json_object)


