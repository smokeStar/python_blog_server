# 文件配置 2018-04-21
from flask import Blueprint, current_app
import sys

sys.path.append("..")
import run

api = Blueprint('api', __name__)


with run.app.app_context():
	from .hook import before
	from .api import login, logout, register, send_cap, weibologin