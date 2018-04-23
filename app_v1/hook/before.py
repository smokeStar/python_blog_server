# 钩子函数 --2018-04-21

from ..model.engine import User, db_session
from flask import request, g, current_app
from ..__init__ import api

# 在每次请求前调用
@api.before_request
def before_request():
	print("before request")
	token = request.headers.get('token')
	phone_number = current_app.redis.get('token:%s'%token)
	if phone_number:
		g.current_user = db_session.query(User).filter_by(phone_number=phone_number).first()
		g.token = token
	return
