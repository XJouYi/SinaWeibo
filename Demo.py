#!/usr/bin/python
# -*- coding: utf-8 -*-
from weibo import Weibo
import time


if __name__ == '__main__':
    wb= Weibo("account","password")
    wb.postMessage("0.2测试1:文本")
    time.sleep(1)
    wb.postImage("0.2测试2:一张图片","/Downloads/4.png")
    time.sleep(1)
    wb.postImage("0.2测试3:多张图片","/Downloads/4.png","/Downloads/5.jpg")

    blogList = wb.getMyBlogList(1)
    for blog in blogList:
        print(blog)

