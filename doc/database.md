数据库迁移

数据库迁移可能会导致数据丢失、损坏！！！
要提前备份！！！

初始化
python manage.py db init
创建版本
python manage.py db migrate -m ""
更新
python manage.py db upgrade
