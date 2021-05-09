import unittest
from unittest.mock import Mock
from run import sqlcon, etcd_data_to_sql,etcd_data_to_json,etcd_connect
from colorama import Fore, Back, Style
class TestDb(unittest.TestCase):
    def setUp(self):
        self.db = sqlcon('test')
        self.obj = etcd_connect('127.0.0.1','2379')

    def test_etcd_data_to_sql(self):
        try:
            etcd_data_to_sql(self.obj,self.db)
            self.db.execute("SELECT * from etcd")
            print(Back.GREEN+"Test etcd_data_to_sql Successfully!")
        except:
            print(Fore.RED +"Test etcd_data_to_sql FAIL")
    def test_etcd_data_to_json(self):
        try:
            etcd_data_to_json(self.obj,'data')
            print(Back.GREEN+"Test test_etcd_data_to_json Successfully!")
        except:
            print(Fore.RED +"Test test_etcd_data_to_json FAIL")
if __name__ == '__main__':
    unittest.main()