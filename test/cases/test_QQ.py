#coding = utf-8

import requests, unittest


class TestQQ(unittest.TestCase):
    """测试QQ"""

    def testQQN(self):
        """测试QQ用例"""
        url = "http://japi.juhe.cn/qqevaluate/qq"
        par = {
               'key': '8dbee1fcd8627fb6699bce7b986adc45',
               'qq': '501230183'
               }
        r = requests.get(url, par)
        res = r.json()['reason']
        self.assertTrue(res == 'success')


if __name__ == '__main__':
    unittest.main()