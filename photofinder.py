#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import os

# import xhhub

targetPath = r'D:\python\jwtsphotos\photos'
url = 'http://jwts.hit.edu.cn/xswhxx/showPhoto?xh='
idsPath = r'D:\python\jwtsphotos'

def saveFile(xh, data):
    targetPath = r'D:\python\jwtsphotos\photos'
    tmp = str(xh)[:6]
    tmp = tmp[:3] + '_' + tmp[3:]
    targetPath = os.path.join(targetPath, tmp)
    if not os.path.isdir(targetPath):
        os.mkdir(targetPath)
    filePath = os.path.join(targetPath, xh + '.jpeg')
    with open(filePath, 'wb') as f:
        f.write(data)
    print('成功:保存于%s\n' % filePath)

def tryxh(xh):
    print('尝试学号: %s' % xh)
    getUrl = url + xh
    print(getUrl)
    cookie = 'name=value; JSESSIONID=nbbDhTJKVLV5Vh0fFLvc0cBvnp8zZjHkzvYQNfQ1nZzymG8QSpW2!1197360304; clwz_blc_pst=33558700.24859; name=value'
    # cookie = input('Input cookie:')
    headers = {'Cookie': cookie}
    req = urllib.request.Request(getUrl, None, headers)
    try:
        data = urllib.request.urlopen(req).read()
    except:
        print('网络错误！')
        os._exit(1)
    # print(data)

    if data.decode('utf-8', errors='ignore').find('<script') == 0:
        print('Cookie过期！\n',data)
        os._exit(2)
    else:
        saveFile(xh, data)
    # urllib.request.urlretrieve(url + xh, filePath(xh))


if __name__ == '__main__':
    idsfile = []
    # idsfile = [c for c in os.listdir(idsPath) if c.find('ver') > -1]
    # idsfile = ['ver_116100.txt']
    xh = []
    for c in idsfile:
        p = os.path.join(idsPath, c)
        with open(p, 'r') as f:
            line = f.readline()
            while line:
                line = line.strip('\n')
                xh.append(line)
                line = f.readline()
    print('待抓取学号(%s)：' % len(xh), xh)
    for c in xh:
        tryxh(c)