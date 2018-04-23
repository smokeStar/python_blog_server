# https://api.weibo.com/oauth2/authorize?client_id=1981969326&response_type=code&redirect_uri=http%3a%2f%2fwww.wenjian.group
# code = 8cfed44acf386dfd2973dc791c82d6a7
from flask import request, jsonify
from ..__init__ import api
import requests, json

@api.route("/getInfo")
def get_access_token():
	code = request.query_string.decode().split('=')[1]
	url  = "https://api.weibo.com/oauth2/access_token?client_id=1981969326&client_secret=bdb57632f9faf0a74d9771ce554b34e3&grant_type=authorization_code&redirect_uri=http%3a%2f%2fwww.wenjian.group&code="+code
	postData = {}
	try:
		response = requests.post(url, data=json.dumps(postData))
		print(response.text)
		if response.status_code == 200:
			access_token = json.loads(response.text)['access_token']
			return jsonify({"result":True, "access_token":access_token})
		else:
			return jsonify({"result":False, "message":"请求失败1"})
	except requests.RequestException as e:
		return jsonify({"result":False, "message":"请求失败2"})



