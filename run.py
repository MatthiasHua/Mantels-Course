'''
启动器
config: [Net]IP 向指定ip开放, '0.0.0.0'：向所有ip开放
生产环境中应确保debug关闭
'''

#app: 应用实例
#config: 根目录下config.ini
from app import app, config

# 调试模式： '0.0.0.0',debug = True
app.run(config.get("Net", "IP"), debug=True)
