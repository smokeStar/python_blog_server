from flask import request,jsonify,current_app
from functools import wraps  # wraps(f)的作用是保留原有函数的名称

def login_check(f):
	@wraps(f)
	def decorator():
		token = request.headers.get('token')
		if not token:
			return jsonify({'result': False, 'message': '需要验证'})
		phone_number = current_app.redis.get('token:%s' % token)

		if not phone_number or token != current_app.redis.hget('user:%s' % phone_number, 'token'):
			return jsonify({'result': False, 'message': '验证信息错误'})
		return f()
	return decorator	
