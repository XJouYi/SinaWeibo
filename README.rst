# SinaWeibo
>python3脚本,非官方API实现登录新浪微博发送消息和图片

## 安装
> pip install sinaweibo

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
>pip install requests

>pip install rsa

>pip install beautifulsoup4


