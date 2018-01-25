# SinaWeibo
>1.python脚本,支持非官方API 方式登录新浪微博发送消息和图片

>2.python2.7版在[https://github.com/XJouYi/SinaWeibo/releases/tag/v0.1]

## API
| Name|Params|Remark|
| --------   | -----:  | :----: |
| uploadPic  | picPath                |上传图片|
| postMessage| message                |发送文本微博|
| postImage  | message,*picPaths      |发送文本加图片(图片可多张)|
| getFollowList  | pageNum      |获取我的关注|
| getFansList  | pageNum      |获取我的粉丝|
| getMyBlogList  | pageNum      |获取我的微博|

## Demo
>Demo.py

## 依赖库
>pip3 install requests

>pip3 install rsa

>pip3 install beautifulsoup4



