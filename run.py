import etcd3
import json
etcd = etcd3.client(host='127.0.0.1', port=2379)

json_dic ={}
for value, metadata in etcd.get_all():
    json_dic.update({metadata.key.decode('utf-8'):value.decode('utf-8')})

json_object=json.dumps(json_dic)
print(json_object)


