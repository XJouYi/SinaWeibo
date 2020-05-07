# -*- coding: utf-8 -*-

from SinaWeibo import Weibo
import wx
import win32api
import sys, os

APP_TITLE = u'微博客户端'


class mainFrame(wx.Frame):
    wbClient = None
    '''程序主窗口类，继承自wx.Frame'''

    def __init__(self, parent):
        '''构造函数'''

        wx.Frame.__init__(self, parent, -1, APP_TITLE)
        self.SetBackgroundColour(wx.Colour(224, 224, 224))
        self.SetSize((600, 400))
        self.Center()

        wx.StaticText(self, -1, u'用户名', pos=(10, 55), size=(42, -1))
        wx.StaticText(self, -1, u'密码', pos=(10, 85), size=(40, -1))

        self.tc1 = wx.TextCtrl(self, -1, '', pos=(50, 50), size=(150, -1), name='TC01', style=wx.TE_PASSWORD)
        self.tc2 = wx.TextCtrl(self, -1, '', pos=(50, 80), size=(150, -1), name='TC02', style=wx.TE_PASSWORD)

        btn_login = wx.Button(self, -1, u'登录', pos=(200, 50), size=(100, 25))
        btn_login.Bind(wx.EVT_LEFT_DOWN, self.OnLoginWeibo)

        wx.StaticText(self, -1, u'内容', pos=(10, 125), size=(40, -1))
        self.tcContent = wx.TextCtrl(self, -1, '', pos=(50, 120), size=(200, -1))

        wx.StaticText(self, -1, u'图片', pos=(10, 155), size=(40, -1))
        self.tcImage = wx.TextCtrl(self, -1, '', pos=(50, 150), size=(200, -1))

        btn_content = wx.Button(self, -1, u'发送文本微博', pos=(50, 180), size=(100, 25))
        btn_content.Bind(wx.EVT_LEFT_DOWN, self.OnPostContent)

        btn_image = wx.Button(self, -1, u'发送图文微博', pos=(150, 180), size=(100, 25))
        btn_image.Bind(wx.EVT_LEFT_DOWN, self.OnPostImage)

        btn_blog = wx.Button(self, -1, u'获取微博', pos=(250, 180), size=(100, 25))
        btn_blog.Bind(wx.EVT_LEFT_DOWN, self.OnGetBlogs)

        wx.StaticText(self, -1, u'删除ID', pos=(10, 235), size=(40, -1))
        self.tcBlogID = wx.TextCtrl(self, -1, '', pos=(50, 230), size=(200, -1))

        btn_del = wx.Button(self, -1, u'删除微博', pos=(50, 260), size=(100, 25))
        btn_del.Bind(wx.EVT_LEFT_DOWN, self.OnDelBlog)


    def OnLoginWeibo(self,evt):
        self.wbClient = Weibo(self.tc1.GetValue(), self.tc2.GetValue())

    def OnPostContent(self,evt):
        self.wbClient.postMessage(self.tcContent.GetValue())

    def OnPostImage(self,evt):
        self.wbClient.postImage(self.tcContent.GetValue(), self.tcImage.GetValue())

    def OnGetFans(self,evt):
        pageNum = 1
        fansList , hasNext = self.wbClient.getFansList(pageNum)
        print(fansList)
        while hasNext == True:
            pageNum = pageNum + 1
            fansList, hasNext = self.wbClient.getFansList(pageNum)
            print(fansList)

    def OnGetBlogs(self,evt):
        for num in range(0,10):
            blogList = self.wbClient.getMyBlogList(num)
            for blog in blogList:
                print(blog)

    def OnDelBlog(self,evt):
        delResp = self.wbClient.detBlog(self.tcBlogID.GetValue())
        print(delResp.text)



class mainApp(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = mainFrame(None)
        self.Frame.Show()
        return True


if __name__ == "__main__":
    app = mainApp()
    app.MainLoop()
