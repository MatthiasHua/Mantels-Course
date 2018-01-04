from flask import render_template, redirect, url_for, request
#根目录下config.ini
from app import config
#installation蓝图应用
from app.installation import installation

#安装包管理
@installation.route('/packagemanager', methods=['POST', 'GET'])
def packagemanager():
	#是否已同意许可证协议
	license_config = {'True': packagemanager_already_accept, 'False': pacekagemanager_new}
	#返回view
	return license_config[config.get("License", "License")](request)

#已同意许可证协议
def packagemanager_already_accept(request):
	#映射接收到的请求
	packagemanager_request = {'GET': packagemanager_get, 'POST': packagemanager_post}
	return packagemanager_request[request.method](request)

#收到GET请求
def packagemanager_get(request):
	return render_template("packagemanager.html",
		infolist_base = infolist("Base"),
		infolist_application = infolist("Application"),
		enablelist_base = enablelist("Base"),
		enablelist_application = enablelist("Application"))

#收到POST请求
def packagemanager_post(request):
	#通过HTTP POST表单更新设置
	applyconfig("Base", request.form.getlist('base[]'))
	applyconfig("Application", request.form.getlist('application[]'))	
	#返回完成信息		
	return "Done"


#未同意许可证协议
def pacekagemanager_new(request):
	return redirect(url_for("installation.license"))

#key：Base/Application
#返回对应类型模块的属性信息
def infolist(key):
	#模块名称列表
	applist = [i.capitalize() for i,j in config.items(key)]
	#每个模块的属性
	propertylist =  ["Name", "Vision", "Description", "Index"]

	#闭包函数 x为模块名称 y为属性名称
	def func_1(x):
		def func_2(y):
			return config.get(x, y)
		return func_2
	#返回第i个模块的属性列表
	def func_3(i):
		func = func_1(applist[i])
		return list(map(func, propertylist))
	#返回模块属性信息
	return list(map(func_3, range(len(applist))))

#返回列表 每个模块是否启用
#e.g. ['True', 'Fasle', 'False']
def enablelist(key):
    return [b for a,b in config.items(key)]

#key：Base/Application
#changelist: 每个模块是否启用
#应用设置
def applyconfig(key, changelist):
	#当前设置
	old = config.items(key)

	#修改第i个模块的设置
	def func(i):
		if old[i][1] != changelist[i].capitalize():
			#修改设置
			config.set(key, old[i][0] , changelist[i].capitalize())
			#保存到设置文件
			config.write(open('config.ini', 'w'))

	#应用于所有模块
	list(map(func, range(len(old))))