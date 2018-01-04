import logging

#############
#文件日志记录#
#############
#打印岛文件日志的最低级别
logging.basicConfig(level=logging.DEBUG,
#信息格式
format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#时间格式
datefmt='%a, %d %b %Y %H:%M:%S',
#日志文件名称
filename='main.log',
filemode='w')

#############
#屏幕实时打印#
#############
console = logging.StreamHandler()
#实时显示的日志的最低级别
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

