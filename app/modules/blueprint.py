#蓝图管理

from app import app
#日志
from app.logging import logging
#导入蓝图模块
def import_flask_blueprint(bp):
    logging.info(" * Import module:" + bp[0])
	#import模块
    bpmodule = __import__("app." + bp[0], globals(), locals(), list(bp[0]))
    #获取应用实例
    bpapp = getattr(bpmodule, bp[0])
    #通过蓝图挂载应用实例
    app.register_blueprint(bpapp, url_prefix = "/" + bp[0])
