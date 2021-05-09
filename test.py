import unittest
from run import sqlcon, etcd_data_to_sql,etcd_data_to_json,etcd_connect

class TestDb(unittest.TestCase):
    def setUp(self):
        self.db = sqlcon('test')
        self.obj = etcd_connect('127.0.0.1','2379')
    def test_etcd_data_to_sql(self):
        try:
            etcd_data_to_sql(self.obj,self.db)
            user = self.db.execute("SELECT * from etcd")
            print(f"Test etcd_data_to_sql Successfully!")
        except:
            print(f"Test etcd_data_to_sql FAIL")
    def test_etcd_data_to_json(self):
        pass
if __name__ == '__main__':
    unittest.main()