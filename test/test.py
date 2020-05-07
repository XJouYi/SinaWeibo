#!/usr/bin/python
# -*- coding: utf-8 -*-
from SinaWeibo import Weibo

if __name__ == '__main__':
    wb = Weibo("", "")
    # wb.postMessage("0.3测试1:文本")
    # wb.postImage("0.2测试2:一张图片", "/Downloads/4.png")
    # wb.postImage("0.2测试3:多张图片", "/Downloads/4.png", "/Downloads/5.jpg")

    # 我的关注
    # pageNum = 1
    # followList, hasNext = wb.getFollowList(pageNum)
    # print(followList)
    # while hasNext == True:
    #     pageNum = pageNum + 1
    #     followList, hasNext = wb.getFollowList(pageNum)
    #     print(followList)

    # 我的粉丝
    pageNum = 1
    fansList , hasNext = wb.getFansList(pageNum)
    print(fansList)
    while hasNext == True:
        pageNum = pageNum + 1
        fansList, hasNext = wb.getFansList(pageNum)
        print(fansList)

    # 我的微博
    # for pageNum in range(0, 30):
    #     blogList = wb.getMyBlogList(pageNum)
    #     for blog in blogList:
    #         print(blog)
            # delResp = wb.detBlog(blog.id)
            # print(delResp.text)

    # 删除微博
