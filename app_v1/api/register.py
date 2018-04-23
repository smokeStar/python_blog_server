# register接口 --2018-4-21
import requests, datetime, hashlib, base64, json, random, redis, re, json
from flask import request, jsonify, current_app
from ..model.engine import User, db_session
from ..__init__ import api



def v_phone_num(phone_num):
	p = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
	print(p.match(phone_num))
	if not phone_num or not p.match(phone_num):
		return "手机号码格式错误"
	else:
		return None
def v_cap(phone, cap):
	if not cap or cap != current_app.redis.get('phone:%s'%phone):
		return "验证码错误"
	else:
		return None
def v_nickName(nickname):
	if not nickname:
		return "昵称不能为空"
	else:
		return None
def v_password(password):
	if not password:
		return "密码不能为空"
	else:
		return None

def query_isRegister(phone_number):
	result = db_session.query(User).filter_by(phone_number=phone_number).first()
	if result:
		return "账号已存在"
	else:
		return None



@api.route('/register', methods=["POST"])
def register():
	data 		 = json.loads(request.data)
	phone_number = data.get('phone_number')
	password     = data.get('password')
	cap          = data.get('cap')
	nickname     = data.get('nickname')

	err = v_phone_num(phone_number ) or v_password(password) or v_cap(phone_number,cap) or v_nickName(nickname)
	if err:
		return jsonify({ 'result':False, 'message':err })
	else:
		if query_isRegister(phone_number):
			return jsonify({ 'result':False, 'message': "账号已注册" })
		else:
			obj = User(phone_number=phone_number, password=password, nickname=nickname)
			db_session.add(obj)
			db_session.commit()
			return jsonify({ 'result':True, 'message': "注册成功" })
