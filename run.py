import etcd

client = etcd.Client() # this will create a client against etcd server running on localhost on port 4001
client = etcd.Client(port=2379)
client = etcd.Client(host='192.168.49.2', port=2379)
client = etcd.Client(host='192.168.49.2', port=2379, allow_redirect=False) # wont let you run sensitive commands on non-leader machines, default is true
client = etcd.Client(
             host='192.168.49.2',
             port=2379,
             allow_reconnect=True,
             protocol='https',)
# client.read('/nodes/n2').value
# #recursively read a directory
# r = client.read('/nodes', recursive=True, sorted=True)
# for child in r.children:
#     print("%s: %s" % (child.key,child.value))

# client.read('/nodes/n2', wait=True) #Waits for a change in value in the key before returning.
# client.read('/nodes/n2', wait=True, waitIndex=10)

# # raises etcd.EtcdKeyNotFound when key not found
# try:
#     client.read('/invalid/path')
# except etcd.EtcdKeyNotFound:
#     # do something
#     print ("error")