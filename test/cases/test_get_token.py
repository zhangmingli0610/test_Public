# coding = utf-8

import unittest
import requests


class TestDRaaS(unittest.TestCase):
    """测试DRaaS"""
    def testGetToken1(self):
        """成功获取token"""
        url = 'http://221.122.78.198:8092/api/auth/token'
        body = {
            'username': 'admin',
            'password': 'admin123456',
            'fromSource': 'operate'
        }
        r = requests.post(url, json=body)
        res = r.json()['msg']
        self.assertTrue(res == '获得token成功')

    def testGetToken2(self):
        """用户名不存在或密码错误"""
        url = 'http://221.122.78.198:8092/api/auth/token'
        body = {
            'username': 'admin',
            'password': 'admin',
            'fromSource': 'operate'
        }
        r = requests.post(url, json=body)
        res = r.json()['msg']
        self.assertTrue(res == '用户名不存在或密码错误')


if __name__ == '__main__':
    unittest.main()
