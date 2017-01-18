#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import base64
import binascii
import rsa
import re
import json
import time
import os
import random
from ConfigUtils import Config

class Weibo(object):
    WBCLIENT = 'ssologin.js(v1.4.18)'
    user_agent = (
	    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) '
        'Chrome/20.0.1132.57 Safari/536.11'
    )
    def __init__(self,config):
        self.config = config
        self.session = requests.session()
        self.session.headers = {
            "User-Agent":Weibo.user_agent
        }
        self.login()
    def encrypt_passwd(self,passwd, pubkey, servertime, nonce):
        key = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(passwd)
        passwd = rsa.encrypt(message.encode('utf-8'), key)
        return binascii.b2a_hex(passwd)

    def login(self):
        login = self.config.Login
        password = self.config.Password
        self.userName = self.config.UserName

        resp = self.session.get(
            'http://login.sina.com.cn/sso/prelogin.php?'
            'entry=weibo&callback=sinaSSOController.preloginCallBack&'
            'su=%s&rsakt=mod&checkpin=1&client=%s' %
            (base64.b64encode(login.encode('utf-8')), Weibo.WBCLIENT)
        )

        pre_login_str = re.match(r'[^{]+({.+?})', resp.text).group(1)
        pre_login = json.loads(pre_login_str)
        data = {
            'entry': 'weibo',
            'gateway': 1,
            'from': '',
            'savestate': 7,
            'userticket': 1,
            'ssosimplelogin': 1,
            'su': base64.b64encode(requests.utils.quote(login).encode('utf-8')),
            'service': 'miniblog',
            'servertime': pre_login['servertime'],
            'nonce': pre_login['nonce'],
            'vsnf': 1,
            'vsnval': '',
            'pwencode': 'rsa2',
            'sp': self.encrypt_passwd(password, pre_login['pubkey'],
                                pre_login['servertime'], pre_login['nonce']),
            'rsakv' : pre_login['rsakv'],
            'encoding': 'UTF-8',
            'prelt': '53',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.si'
            'naSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        resp = self.session.post(
            'http://login.sina.com.cn/sso/login.php?client=%s' % Weibo.WBCLIENT,
            data=data
        )
        
        login_url = re.search('replace\\(\'([^\']+)\'\\)', resp.text).group(1) 

        resp = self.session.get(login_url)
        login_str = login_str = re.search('\((\{.*\})\)', resp.text).group(1)

        login_info = json.loads(login_str)
        uniqueid = login_info["userinfo"]["uniqueid"]
        self.uid = uniqueid.encode("ascii")
        print("登录成功 uid:"+self.uid)
        
    def postData(self,data):
        currTime = "%d" % (time.time()*1000)
        self.session.headers["Host"]="weibo.com"
        self.session.headers["Origin"]="http://weibo.com"
        Referer = "http://www.weibo.com/u/%s/home?wvr=5" % self.uid
        self.session.headers["Referer"] = Referer
        resp = self.session.post(
            'http://weibo.com/aj/mblog/add?ajwvr=6&__rnd=%s'%currTime,data = data
        )

    def postMessage(self,message):
        data = {
            'location':'v6_content_home',
            'text':message,
            'appkey':'',
            'style_type':1,
            'pic_id':'',
            'pdetail':'',
            'rank':0,
            'rankid':'',
            'module':'stissue',
            'pub_source':'main_',
            'pub_type':'dialog',
            '_t':0
        }
        self.postData(data)
        print(message +" 发送成功")
        
    def postImage(self,message,filePath):
        file = open(filePath, 'r')
        payload = file.read()
        file.close()
        url = 'weibo.com/u/'+self.uid
        atName = "@"+self.userName
        
        self.session.headers["Referer"] = "http://js.t.sinajs.cn/t6/home/static/swf/MultiFilesUpload.swf?version=446d5fa804a6fbf9"
        self.session.headers["Host"]="picupload.service.weibo.com"
        self.session.headers["Origin"]="http://js.t.sinajs.cn"
        resp = self.session.post(
            'http://picupload.service.weibo.com/interface/pic_upload.php?app=miniblog'+
            '&data=1&url='+url+'&markpos=1&logo=1&nick='+atName+'&marks=1&url='+url+
            '&mime=image/png&ct='+str(random.random()),
            data=payload
            )
        
        resultStr = re.search('{"code.*', resp.text).group(0)
        resultJson = json.loads(resultStr)
        pic_id = resultJson["data"]["pics"]["pic_1"]["pid"]
        data = {
            'location':'v6_content_home',
            'text':message,
            'appkey':'',
            'style_type':1,
            'pic_id':pic_id,
            'pdetail':'',
            'rank':0,
            'rankid':'',
            'module':'stissue',
            'pub_source':'main_',
            'pub_type':'dialog',
            '_t':0
        }
        self.postData(data)
        print(message +" 发送成功")
        
if __name__ == '__main__':
    weibo = Weibo(Config())
    weibo.postMessage('你好')
    weibo.postImage('分享图片2','/Users/jinyi/Downloads/3.png')
    # weibo.postMessage("hello,world")
    # file = open('/Users/jinyi/Downloads/1.png', 'r')
    # all_the_text = file.read()
    # print(all_the_text)
    # for byte in all_the_text:
    #     temp = binascii.b2a_hex(byte)
    # file.close()
    print('Finish')
    
        