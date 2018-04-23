# logout接口 --2018-4-21
from ..utlis.decoration import login_check
from flask import g, current_app, jsonify
from ..__init__ import api

@api.route('/logout')
@login_check
def logout():
	user = g.current_user
	current_app.redis.delete('token:%s'%g.token)
	current_app.redis.hmset('user:%s'%user.phone_number, { 'app_online':0 })
	return jsonify({ 'result':True, 'message':'注销成功' })
