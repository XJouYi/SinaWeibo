#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json


class Config(object):
    def __init__(self):
        path = sys.path[0] + "/config.json"
        configFile = open(path,'r')
        try:
            configJson = json.load(configFile)
            self.Login = configJson["WeiboLogin"]
            self.Password = configJson["WeiboPassWord"]
            self.UserName = configJson["WeiboUserName"]
        except Exception as e:
            print(e)
        finally:
           configFile.close() 
           
if __name__ == '__main__':
    config = Config()
    print(config.Login)
    print(config.Password)
    print(config.UserName)
            

    