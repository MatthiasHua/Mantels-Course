from flask import Blueprint, render_template, redirect, url_for, request, session, make_response
#根目录下config.ini
from app import config
#数据库模型
from app.model import *
from app import db
from app.modules.courseware import *
import time
#创建应用实例
experiment = Blueprint('experiment', __name__,  template_folder='templates')

leftbarlist = (("guide", "实验指导"),\
               ("result", "实验结果"))

@experiment.route('/id/<int:id>', methods=['POST', 'GET'])
@experiment.route('/id/<int:id>/index', methods=['POST', 'GET'])
@experiment.route('/id/<int:id>/guide', methods=['POST', 'GET'])
def edit_experiment_guide(id):
    experiment = Experiment.query.filter_by(id = id).first()
    return render_template("experiment_guide.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    guide = experiment.guide,\
    id = id,\
    leftbar = leftbarlist,\
    active = 0)


@experiment.route('/id/<int:id>/result', methods=['POST', 'GET'])
def edit_experiment_result(id):
    results = ExperimentResult.query.filter_by(student_id = session['id']).all()
    experiment = Experiment.query.filter_by(id = id).first()
    return render_template("experiment_result.html",\
    role = session.get('role', 'unknow'),\
    username = session.get('username', ''),\
    result = experiment.result,\
    id = id,\
    leftbar = leftbarlist,\
    results = results,\
    active = 1)
