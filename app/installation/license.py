from flask import render_template, redirect, url_for, request
#根目录下config.ini
from app import config
#installation蓝图应用
from app.installation import installation

#许可证协议
@installation.route('/license', methods=['POST', 'GET'])
def license():
	#是否已接受协议
	license_config = {'True': license_already_accept, 'False': lincese_new}
	#返回view
	return license_config[config.get("License", "License")](request)

#收到GET请求
def license_get(request):
	return render_template("License.html", url1 = url_for("installation.packagemanager"))

#收到POST请求
def license_post(request):
	#检查HTTP POST表单
	if request.form['license'] == "accepted":
		#更改设定
		config.set("License", "License", "True")
		#写入设定
		config.write(open('config.ini', 'w'))
	#返回完成信息
	return "Done"

#已同意许可证协议
def license_already_accept(request):
	#无需再次同意协议，直接跳转至安装包管理页面
	return redirect(url_for("installation.packagemanager"))

#未同意许可证协议
def lincese_new(request):
	#映射接收到的请求
	license_request = {'GET': license_get, 'POST': license_post}
	#返回view
	return license_request[request.method](request)
