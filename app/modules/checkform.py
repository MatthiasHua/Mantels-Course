#表单验证库

#新建课程的表单的验证
#需要对表单进行验证
#现在只简单确认表单不为空
#返回1代表合法
#小于0代表不合法
#返回原因
#-1为未知或还没有设置的错误
def checkform_new_course(form):
    if form.get('coursename', '') == '':
        return -1
    if form.get('courseid', '') == '':
        return -1
    if form.get('start', '') == '':
        return -1
    if form.get('end', '') == '':
        return -1
    if form.get('introduction', '') == '':
        return -1
    if form.get('id', '') == '':
        return -1
    return 1
