# 启动文件 2018-04-20
from flask import Flask
from app_v1.config.config import Conf
import redis

app = Flask(__name__)

def create_app():
	app.config.from_object(Conf)
	app.config['JSON_AS_ASCII'] = False  # jsonify显示中文

 	# 连接redis处理token,decode_responses设置为true时读取redis中的数据时返回的是str,而不是二进制数据
	app.redis = redis.Redis(host=app.config["REDIS_HOST"],port=app.config["REDIS_PORT"], db=app.config["REDIS_DB"], charset='utf-8', decode_responses=True)
	app.config.debug = app.config["DEBUG"]
	
	from app_v1.__init__ import api as api_v1_blueprint
	app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

	return app


if __name__ == '__main__':
	app = create_app()
	app.run(debug=app.config.debug)