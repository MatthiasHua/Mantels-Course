# Mantels | Course

- 轻量级课程系统
- 支持Markdown


## 安装

建立虚拟环境:
```
pip install virtualenv
virtualenv flask
```

建立环境:
```
flask\Scripts\pip install -r requirements.txt(Windows)
flask/bin/pip install -r requirements.txt(Linux)
```

建议使用国内源
```
pip install -i <url>
```

清华：https://pypi.tuna.tsinghua.edu.cn/simple

阿里云：http://mirrors.aliyun.com/pypi/simple/

中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/

华中理工大学：http://pypi.hustunique.com/

山东理工大学：http://pypi.sdutlinux.org/

豆瓣：http://pypi.douban.com/simple/

## 更新日志

### beta v1.2更新内容:

----

- 增加 部分api支持
- 增加 邮箱系统
- 增加 用户邮箱验证
- 增加 在课程中发布公告
- 增加 markdown图片缩放(拓展功能, 非markdown标准内容)
- 增加 google analytics
- 增加 人脸识别(测试)
- 修复 markdown中图片溢出
- 修复 部分页面logo显示错误

api部分:
- access_key(教室功能, 需要在个人中心开启)
- 学生二维码登录
详情见[文档中心](http://doc.mantels.top)

### beta v1.1更新内容:

----

- 增加 微信课件
- 增加 微信后台消息处理
- 增加 课件部分按钮功能
- 修复 权限认证
- 修复 Markdown部分标签显示错误
- 优化 入口程序结构
- 优化 功能模块库
- 优化 主页
