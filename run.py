import etcd

client = etcd.Client() # this will create a client against etcd server running on localhost on port 4001
client = etcd.Client(port=4002)
client = etcd.Client(host='127.0.0.1', port=2379)
client = etcd.Client(host=(('127.0.0.1', 2379)))
client = etcd.Client(host='127.0.0.1', port=2379, allow_redirect=False) # wont let you run sensitive commands on non-leader machines, default is true
# If you have defined a SRV record for _etcd._tcp.example.com pointing to the clients
client = etcd.Client(srv_domain='example.com', protocol="https")
# create a client against https://api.example.com:443/etcd
client = etcd.Client(host='api.example.com', protocol='https', port=443, version_prefix='/etcd')