from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
from app.modules.courseware import *
import time
#创建应用实例
editexperiment = Blueprint('editexperiment', __name__,  template_folder='templates')

leftbarlist = (("guide", "实验指导"),\
               ("result", "实验结果"),\
               ("testresultdata", "测试数据"))

@editexperiment.route('/id/<int:id>', methods=['POST', 'GET'])
@editexperiment.route('/id/<int:id>/index', methods=['POST', 'GET'])
@editexperiment.route('/id/<int:id>/guide', methods=['POST', 'GET'])
def edit_experiment_guide(id):
    experiment = Experiment.query.filter_by(id = id).first()
    return render_template("edit_experiment_guide.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    guide = experiment.guide,\
    id = id,\
    leftbar = leftbarlist,\
    active = 0)

@editexperiment.route('/id/<int:id>/editguide', methods=['POST', 'GET'])
def edit_guide(id):
    if request.form.get('guide', '') != '':
        experiment = Experiment.query.filter_by(id = id).first()
        experiment.guide = request.form['guide']
        db.session.commit()
        return 'Done'
    return '233'

@editexperiment.route('/id/<int:id>/result', methods=['POST', 'GET'])
def edit_experiment_result(id):
    results = ExperimentResultteacher.query.filter_by(teacher_id = session['id']).all()
    experiment = Experiment.query.filter_by(id = id).first()
    return render_template("edit_experiment_result.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    result = experiment.result,\
    id = id,\
    leftbar = leftbarlist,\
    results = results,\
    active = 1)

@editexperiment.route('/id/<int:id>/editresult', methods=['POST', 'GET'])
def edit_result(id):
    if request.form.get('result', '') != '':
        experiment = Experiment.query.filter_by(id = id).first()
        experiment.result = request.form['result']
        db.session.commit()
        return 'Done'
    return '233'

@editexperiment.route('/id/<int:id>/testresultdata', methods=['POST', 'GET'])
def testresultdatat(id):
    results = ExperimentResultteacher.query.filter_by(teacher_id = session['id']).all()
    return render_template("edit_experiment_data.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    id = id,\
    leftbar = leftbarlist,\
    results = results,\
    active = 2)

@editexperiment.route('/id/<int:id>/adddata', methods=['POST', 'GET'])
def add_data(id):
    experiment = Experiment.query.filter_by(id = id).first()
    if request.form.get('index', '') != '' and request.form.get('content', '') != '':
        newresult = ExperimentResultteacher(request.form['index'], id, experiment.class_id, session['id'], request.form['content'], int(time.time()))
        db.session.add(newresult)
        db.session.commit()
        return 'Done'
    return '233'
