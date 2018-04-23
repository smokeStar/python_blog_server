# 发送验证码接口 --2018-4-21
import requests, datetime, hashlib, base64, json, random, re
from .register import v_phone_num, query_isRegister
from flask import current_app, jsonify, request
from ..__init__ import api

accountSid = "8a216da862dc09140162dc8d21de007f"
token      = "3bc3de791bab4f81b4e446a1a4fc4566"

def send_message(phone):
	validate_num = str(random.randint(1000,9999))
	tiemstamp    = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	m 			 = hashlib.md5()
	m.update(accountSid.encode('utf-8'))
	m.update(token.encode('utf-8'))
	m.update(tiemstamp.encode('utf-8'))
	sigParameter = m.hexdigest().upper()   # md5加密并转大写

	url 		      = "https://sandboxapp.cloopen.com:8883/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s" % (accountSid, sigParameter)
	authorization     = accountSid + ':' + tiemstamp
	bytesString       = authorization.encode(encoding="utf-8")
	new_authorization = base64.b64encode(bytesString).strip() # base64码加密

	header = {
		"Accept" 	    : "application/json",
		"Content-Type"  : "application/json;charset=utf-8",
		"Authorization" : new_authorization
	}
	data = {
		"to"    	: phone,
		"appId" 	: "8a216da862dc09140162dc8d22430085",
		"templateId": "1",
		"datas"		: [validate_num,'10']
	}

	try:
		response = requests.post(url, data=json.dumps(data), headers=header)
		if response.status_code == 200:
			result = json.loads(response.text)
			if result['statusCode'] == "000000":
				pipe_line = current_app.redis.pipeline()
				pipe_line.set("phone:%s"%phone, validate_num)
				pipe_line.expire("phone:%s"%phone, 600)
				pipe_line.execute()
				return True
	except requests.RequestException as e:
		return False
	else:
		return False


@api.route('/sendcap')
def send_cap():

	phone_number = request.query_string.decode().split('=')[1]
	print(phone_number)

	if v_phone_num(phone_number):
		return jsonify({ "result":False, "message":"手机号码格式错误" })
	else:
		if query_isRegister(phone_number):
			return jsonify({ 'result':False, 'message': "账号已注册" })
		else:
			if send_message(phone_number):
				if not current_app.redis.get('phone:%s'%phone_number):
					return jsonify({ "result":False, "message": "验证码已过期,请重新获取" })
				else:
					return jsonify({ "result":True, "cap":current_app.redis.get('phone:%s'%phone_number) })
			else:
				return jsonify({ "result":False, "message":"获取验证码失败"})

