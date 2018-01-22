#!/usr/bin/python
# -*- coding: utf-8 -*-
import base64
import json
import random
import re
import time

import requests

from common import wconfig
from common import utils


class weibo(object):

    logincode = ""
    password = ""
    uid = ""
    homeUrl = ""
    def __init__(self,logincode,password):
        self.logincode = logincode
        self.password = password

        self.session = requests.session()
        self.session.headers = {
            "User-Agent": wconfig.user_agent
        }
        self.__login()


    def __login(self):
        try:
            resp = self.session.get('http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=%s' %
                                    (base64.b64encode(self.logincode.encode('utf-8')), wconfig.WBCLIENT)
            )
            pre_login = json.loads(re.match(r'[^{]+({.+?})', resp.text).group(1))
            resp = self.session.post( 'http://login.sina.com.cn/sso/login.php?client=%s' %
                                      wconfig.WBCLIENT, data=utils.getLoginStructure(self.logincode,self.password,pre_login)
            )
            resp = self.session.get(re.search('replace\\(\'([^\']+)\'\\)', resp.text).group(1))
            login_info = json.loads(re.search('\((\{.*\})\)', resp.text).group(1))
            self.uid = login_info["userinfo"]["uniqueid"]
            print("%s 登录成功"%self.logincode)
            resp = self.session.get("https://weibo.com/")
            self.homeUrl = resp.url
        except Exception as e:
            print("%s 登录失败"%self.logincode)
            raise e

    def __postData(self,data):
        currTime = "%d" % (time.time()*1000)
        self.session.headers["Host"]="weibo.com"
        self.session.headers["Origin"]="https://weibo.com"
        Referer = "https://www.weibo.com/u/%s/home?wvr=5" % self.uid
        self.session.headers["Referer"] = Referer
        resp = self.session.post(
            'https://weibo.com/aj/mblog/add?ajwvr=6&__rnd=%s'%currTime,data = data
        )
        try:
            result, msg = utils.checkResultMessage(resp.content)
            if result == True:
                print("消息发送成功:%s" % data["text"])
            else:
                print("消息发送失败:%s" % msg)
        except Exception as e:
            print("消息发送失败:%s" % data)
            raise e

    def postMessage(self,message):
        self.__postData(utils.getTextStructure(message))

    def uploadPic(self,picPath):
        url = 'weibo.com/u/' + self.uid
        self.session.headers["Referer"] = self.homeUrl
        self.session.headers["Host"] = "picupload.weibo.com"
        self.session.headers["Origin"] = "https://weibo.com"
        resp = self.session.post(
            'https://picupload.weibo.com/interface/pic_upload.php?app=miniblog' +
            '&data=1&url=' + url + '&markpos=1&logo=1&nick=&marks=1&url=' + url +
            '&mime=image/png&ct=' + str(random.random()),
            data=open(picPath, 'rb')
        )
        resultJson = json.loads(re.search('{"code.*', resp.text).group(0))
        return resultJson["data"]["pics"]["pic_1"]["pid"]

    def postImage(self,message,*picPaths):
        picList = []
        for pic in picPaths:
            picList.append(self.uploadPic(pic))
        self.__postData(utils.getImageStructure(message,"|".join(picList),len(picList)))

        