import unittest
from run import sqlcon, etcd_data_to_sql,etcd_data_to_json,etcd_connect

class TestDb(unittest.TestCase):
    def setUp(self):
        self.db = sqlcon('test')
        self.obj = etcd_connect('127.0.0.1','2379')
    def test_etcd_data_to_sql(self):
        etcd_data_to_sql(self.obj,self.db)
        user = self.db.query.filter_by(value='val1')
        self.assertFalse( user , None)
if __name__ == '__main__':
    unittest.main()