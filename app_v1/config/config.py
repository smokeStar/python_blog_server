# 配置文件 --2018-4-21
# 通用配置
class Config(object):
	KEY : "1231231"


# dubug模式
class DevelopmentConfig(Config):

	DEBUG = True

	REDIS_HOST = "localhost"
	REDIS_PORT = 6379
	REDIS_DB   = 0

	MYSQL_INFO = "mysql+pymysql://root:xxxx@127.0.0.1:3306/test?charset=utf8"

# 生产模式
class ProductConfig(Config):

	DEBUG = False

	REDIS_HOST = "localhost"
	REDIS_PORT = 6379
	REDIS_DB   = 0

	MYSQL_INFO = "mysql+pymysql://root:xxxx@127.0.0.1:3306/test?charset=utf8"

Conf = DevelopmentConfig
