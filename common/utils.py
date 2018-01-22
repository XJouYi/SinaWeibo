#!/usr/bin/python
# -*- coding: utf-8 -*-
import binascii
import rsa
import base64
import requests
import json

def encrypt_passwd(passwd, pubkey, servertime, nonce):
    key = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(passwd)
    passwd = rsa.encrypt(message.encode('utf-8'), key)
    return binascii.b2a_hex(passwd)

def getLoginStructure(logincode,password,pre_login):
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
        'sp': encrypt_passwd(password, pre_login['pubkey'], pre_login['servertime'], pre_login['nonce']),
        'rsakv': pre_login['rsakv'],
        'encoding': 'UTF-8',
        'prelt': '53',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.si' 'naSSOController.feedBackUrlCallBack', 'returntype': 'META'
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

def getImageStructure(message,pic_id,picNum):
    data = getTextStructure(message)
    data["pic_id"] = pic_id
    if picNum > 0 :
        data["updata_img_num"] = picNum
    return data

def checkResultMessage(resultJson):
    resultFlag = False
    resultObject = json.loads(resultJson)
    try:
        code = resultObject['code']
        msg = resultObject['msg']
        if code == '100000':
            resultFlag = True
        return resultFlag,msg
    except Exception as e:
        raise e

