# coding = utf-8
import unittest
import ddt
import requests
from util.draas import DRaaS
from config.read_conf import *
from util.readexcel import ExcelUtil
from util import writeexcel

cur_path = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(cur_path, r'config\testdr.xlsx')
excledata = ExcelUtil(file_path, 'Sheet1')
testdata = excledata.dict_data()
case_path = os.path.join(cur_path, r'data\testdr2.xlsx')
writeexcel.copy_excle(case_path)

@ddt.ddt
class Token(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.s = requests.session()
        cls.d = DRaaS(cls.s)
        cls.token = cls.d.get_token(get_value('url'), get_value('username'), get_value('password'))
        write_token(cls.token)

    @ddt.data(*testdata)
    def test_get_view(self, data):
        drill = self.d.drill(get_value('token'))
        res = self.d.get_exe_view(drill, get_value('token'), data)
        self.d.write_res(res, case_path)
        self.assertTrue(data['checkPoint'] in res['msg'])

    def tearDown(self):
        self.s.cookies.clear()

    @classmethod
    def tearDownClass(cls):
        del cls.d

if __name__ == '__main__':
    unittest.main()
