import unittest
from run import sqlcon, etcd_data_to_sql,etcd_data_to_json

class TestDb(unittest.TestCase):
    def setUp(self):
        self.db = sqlcon('test')
        self.obj = {'key1':'val1','key2':'val2','key3':'val3','key4':'val5'}.items()
    def test_etcd_data_to_sql(self):
        etcd_data_to_sql(self.obj,self.db)
        user = self.db.query.filter_by(value='val1')
        self.assertFalse( user , None)
if __name__ == '__main__':
    unittest.main()