#!/usr/bin/python
# -*- coding: utf-8 -*-


import binascii
import rsa
import base64
import requests
import json
from bs4 import BeautifulSoup

from .follow import Follow
from .follow import FollowType
from .fans import Fans
from .blog import Blog


class WbUtils(object):
    @staticmethod
    def encrypt_passwd(passwd, pubkey, servertime, nonce):
        key = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(passwd)
        passwd = rsa.encrypt(message.encode('utf-8'), key)
        return binascii.b2a_hex(passwd)

    @staticmethod
    def getLoginStructure(logincode, password, pre_login):
        data = {
            'entry': 'weibo',
            'gateway': 1,
            'from': '',
            'savestate': 7,
            'userticket': 1,
            'ssosimplelogin': 1,
            'su': base64.b64encode(requests.utils.quote(logincode).encode('utf-8')),
            'service': 'miniblog',
            'servertime': pre_login['servertime'],
            'nonce': pre_login['nonce'],
            'vsnf': 1,
            'vsnval': '',
            'pwencode': 'rsa2',
            'sp': WbUtils.encrypt_passwd(password, pre_login['pubkey'], pre_login['servertime'], pre_login['nonce']),
            'rsakv': pre_login['rsakv'],
            'encoding': 'UTF-8',
            'prelt': '53',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.si' 'naSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        return data

    def getTextStructure(message):
        data = {
            'location': 'v6_content_home',
            'text': message,
            'appkey': '',
            'style_type': 1,
            'pic_id': '',
            'pdetail': '',
            'rank': 0,
            'rankid': '',
            'module': 'stissue',
            'pub_source': 'main_',
            'pub_type': 'dialog',
            'isPri': 0,
            '_t': 0
        }
        return data

    def getImageStructure(message, pic_id, picNum):
        data = WbUtils.getTextStructure(message)
        data["pic_id"] = pic_id
        if picNum > 0:
            data["updata_img_num"] = picNum
        return data

    def checkResultMessage(resultJson):
        resultFlag = False
        resultObject = json.loads(resultJson)
        try:
            code = resultObject['code']
            msg = resultObject['msg']
            data = resultObject['data']
            if code == '100000':
                resultFlag = True
            return resultFlag, msg, data
        except Exception as e:
            raise e

    def getFMViewObjDict(htmlcontent):
        FMViewDict = {}
        soup = BeautifulSoup(htmlcontent, 'html.parser')
        for FMView in soup.find_all('script'):
            FMViewStr = FMView.get_text().strip()
            if FMViewStr.startswith('FM.view('):
                lastIndex = len(FMViewStr) - 1
                if FMViewStr.endswith(';'):
                    lastIndex = lastIndex - 1
                fmObj = json.loads(FMViewStr[8:lastIndex])
                if list(fmObj).__contains__('domid'):
                    FMViewDict[str(fmObj['domid'])] = fmObj
        return FMViewDict

    def getMyInfo(fmDict):
        follow = 0
        fans = 0
        weibo = 0
        try:
            fmhtml = fmDict.get('v6_pl_rightmod_myinfo')['html']
            soup = BeautifulSoup(fmhtml, 'html.parser')
            for a in soup.find_all("a", attrs={"bpfilter": "page_frame", "class": "S_txt1"}):
                strong = a.find('strong')
                if strong != None:
                    nodeType = strong['node-type']
                    if nodeType == 'follow':
                        follow = strong.get_text().strip()
                    if nodeType == 'fans':
                        fans = strong.get_text().strip()
                    if nodeType == 'weibo':
                        weibo = strong.get_text().strip()
            return follow, fans, weibo
        except Exception as e:
            print("获取用户基本信息异常")
            raise e

    def __getPageCount(soup):
        pageCount = 0
        W_pages = soup.find("div", attrs={"class": "W_pages"})
        pageList = W_pages.find_all("a", attrs={"class": "page S_txt1"})
        if len(pageList) > 0:
            pageCount = pageList[-1].get_text().strip()
        return pageCount

    def getFollowList(fmDict):
        followList = []
        fmhtml = fmDict.get('Pl_Official_RelationMyfollow__93')['html']
        soup = BeautifulSoup(fmhtml, 'html.parser')
        for li in soup.find_all("li", attrs={"class": "member_li S_bg1"}):
            node = li.find("a", attrs={"node-type": "screen_name"})
            if node != None:
                if node.attrs.__contains__('usercard'):
                    followList.append(
                        Follow(FollowType.USER, node['usercard'].split('=')[1], node['title'], node['href']))
                else:
                    followList.append(Follow(FollowType.ORG, "", node['title'], node['href']))

        return followList, int(WbUtils.__getPageCount(soup))

    def getFansList(fmDict):
        fansList = []
        fmhtml = fmDict.get('Pl_Official_RelationFans__88')['html']
        soup = BeautifulSoup(fmhtml, 'html.parser')
        for li in soup.find_all("li", attrs={"class": "follow_item S_line2", "node-type": "userItem"}):
            node = li.find("a", attrs={"class": "S_txt1"})
            fansList.append(Fans(node["title"], node["usercard"].split('&')[0].split('=')[0], node["href"]))
        return fansList, int(WbUtils.__getPageCount(soup))

    def getProfileHtml(paramsStr):
        htmlStr = ""
        if paramsStr.startswith("<script>parent.FM.view("):
            htmlStr = json.loads(paramsStr[23:len(paramsStr) - 11])['html']
        return htmlStr

    def getBlogList(htmlContent):
        blogList = []
        soup = BeautifulSoup(htmlContent, 'html.parser')
        for item in soup.find_all("div", attrs={"action-type": "feed_list_item"}):
            mid = item['mid']
            content = item.find("div", attrs={"node-type": "feed_list_content"})
            item_date = item.find("a", attrs={"node-type": "feed_list_item_date"})
            blogList.append(Blog(mid, content.get_text().strip(), item_date.get_text().strip()))
        return blogList


