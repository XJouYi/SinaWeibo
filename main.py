#!/usr/bin/python
# -*- coding: utf-8 -*-
from ConfigUtils import Config
from Weibo import Weibo

if __name__ == '__main__':
    config = Config()
    weibo = Weibo(config)
    weibo.postMessage('你好')
    weibo.postImage('分享图片2','/Downloads/3.png')
    print('Finish')
	

    
    
	