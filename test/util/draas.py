# coding:utf-8

import requests
import re
from util.writeexcel import WriteExcel


class DRaaS(object):
    """
    :describe: 登录DRaaS

    """

    def __init__(self, s):
        self.s = s

    # 获取token
    def get_token(self, url, username, password):
        url = url
        body = {
            'username': username,
            'password': password,
            'fromSource': 'operate'
        }
        try:
            r = self.s.post(url, json=body)
            t = re.findall('token\":\"(.+?)\"', r.content.decode())[0]
        except:
            return 'error'
        return t

    def get_token_is_true(self, token):
        if token != 'error':
            return True
        else:
            return False

    # 访问灾备切换列表
    def drill(self, token):
        url2 = 'http://221.122.78.245:8092/api/app/operate/drill/list'
        h = {'Authorization': token, 'fromSource': 'operate'}
        par = {'page': '1', 'limit': '10', 'name': '', 'status': '', 'vStatus': ''}
        r2 = self.s.get(url2, headers=h, params=par)
        # print(r2.content.decode())
        drillid = r2.json()['data'][0]['id']
        return drillid


    # 查看灾备计划详情
    def get_exe_view(self, drillid, token, testdata):
        url3 = 'http://221.122.78.245:8092/api/app/operate/drill/getExeView'
        par3 = {'id': drillid}
        h3 = {'Authorization': token, 'fromSource': 'operate'}
        res = {'rowNum': '', 'result': '', 'error': '', 'msg': '', 'statuscode': '', 'time': ''}
        try:
            r3 = self.s.get(url3, headers=h3, params=par3)
        except Exception as msg:
            res['error'] = msg
        res['rowNum'] = testdata['rowNum']
        res['statuscode'] = r3.status_code
        res['time'] = str(r3.elapsed.total_seconds())
        try:
            res['msg'] = r3.json()['msg']
        except:
            res['error'] = r3.content.decode()
        if res['msg'] == testdata['checkPoint']:
            res['result'] = "Pass"
        else:
            res['result'] = "Fail    " + r3.content.decode()
        return res

    def write_res(self, res, filename):
        we = WriteExcel(filename)
        we.write(res['rowNum'], 5, res['result'])
        we.write(res['rowNum'], 6, res['error'])
        we.write(res['rowNum'], 7, res['msg'])
        we.write(res['rowNum'], 8, res['statuscode'])
        we.write(res['rowNum'], 9, res['time'])


    def get_exe_view_istrue(self, res):
        if res == '请求成功!':
            return True
        else:
            return False

    host = 'http://221.122.78.245:8092'

if __name__ == '__main__':
    s = requests.session()
    d = DRaaS(s)
    url = 'http://221.122.78.245:8092/api/auth/token'
    username = 'admin'
    password = 'admin123456'
    token = d.get_token(url, username, password)
    print(token)
    drill = d.drill(token)
    testdata = {'rowNum': '3', 'checkPoint': '请求成功!'}
    print(d.get_exe_view(drill, token, testdata))


