# login接口 --2018-4-21
from flask import request, jsonify, current_app
from ..model.engine import User, db_session
import hashlib, time, json
from ..__init__ import api

@api.route('/login', methods=['POST'])
def login():
	# post请求得到的是json字符串,需要转成字典
	data = json.loads(request.data)
	phone_number = data.get("phone_number")
	password     = data.get("password")
	user         = db_session.query(User).filter_by(phone_number=phone_number).first()

	if not user:
		return jsonify({ "result":False, "message":"没有此用户" })
	if user.password != password:
		return jsonify({ "result":False, "message":"密码错误" })

	# md5加密token
	m = hashlib.md5()
	m.update(phone_number.encode('utf-8'))   # md5加密的时候必须先把编码格式显示转化一遍
	m.update(password.encode('utf-8'))
	m.update(str(int(time.time())).encode('utf-8'))
	token = m.hexdigest()

	# 把token存入redis  请求的token先找到phone_number在通过phone_number找到redis中token,相比较
	current_app.redis.hmset('user:%s'%user.phone_number, { 'token':token, 'nickname':user.nickname, 'app_online':1 })
	current_app.redis.set('token:%s'%token, user.phone_number)
	current_app.redis.expire("token:%s"%token, 3600*24*30)

	return jsonify({'result': True, 'message': '登录成功', 'nickname': user.nickname, 'token': token})

