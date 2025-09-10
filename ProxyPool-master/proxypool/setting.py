from os.path import dirname, abspath, join
from environs import Env
from loguru import logger
import shutil


# 模拟platform模块以避免导入错误
def platform():
    class PlatformMock:
        @staticmethod
        def system():
            return "Windows"
    return PlatformMock()

platform = platform()

env = Env()
env.read_env()

# definition of flags
IS_WINDOWS = platform.system().lower() == 'windows'

# definition of dirs
ROOT_DIR = dirname(dirname(abspath(__file__)))
LOG_DIR = join(ROOT_DIR, env.str('LOG_DIR', 'logs'))

# definition of environments
DEV_MODE, TEST_MODE, PROD_MODE = 'dev', 'test', 'prod'
APP_ENV = env.str('APP_ENV', DEV_MODE).lower()
APP_DEBUG = env.bool('APP_DEBUG', True if APP_ENV == DEV_MODE else False)
APP_DEV = IS_DEV = APP_ENV == DEV_MODE
APP_PROD = IS_PROD = APP_ENV == PROD_MODE
APP_TEST = IS_TEST = APP_ENV == TEST_MODE


# Which WSGI container is used to run applications
# - gevent: pip install gevent
# - tornado: pip install tornado
# - meinheld: pip install meinheld
APP_PROD_METHOD_GEVENT = 'gevent'
APP_PROD_METHOD_TORNADO = 'tornado'
APP_PROD_METHOD_MEINHELD = 'meinheld'
APP_PROD_METHOD = env.str('APP_PROD_METHOD', APP_PROD_METHOD_GEVENT).lower()

# redis host - 直接设置为远程Redis服务器
REDIS_HOST = 'redis-11658.crce178.ap-east-1-1.ec2.redns.redis-cloud.com'
# redis port
REDIS_PORT = 11658
# redis password
REDIS_PASSWORD = 'FBb6f5DgnDpUq5vlJHiQqvmO9oIrp6oT'
# redis db
REDIS_DB = 0
# redis connection string
REDIS_CONNECTION_STRING = 'redis://default:FBb6f5DgnDpUq5vlJHiQqvmO9oIrp6oT@redis-11658.crce178.ap-east-1-1.ec2.redns.redis-cloud.com:11658'

# redis hash table key name
REDIS_KEY = env.str('PROXYPOOL_REDIS_KEY', env.str(
    'REDIS_KEY', 'proxies:universal'))

# definition of proxy scores
PROXY_SCORE_MAX = env.int('PROXY_SCORE_MAX', 100)
PROXY_SCORE_MIN = env.int('PROXY_SCORE_MIN', 0)
PROXY_SCORE_INIT = env.int('PROXY_SCORE_INIT', 10)
# whether to get a universal random proxy if no proxy exists in the sub-pool identified by a specific key
PROXY_RAND_KEY_DEGRADED = env.bool('TEST_ANONYMOUS', True)

# definition of proxy number
PROXY_NUMBER_MAX = 50000
PROXY_NUMBER_MIN = 0

# definition of tester cycle, it will test every CYCLE_TESTER second
CYCLE_TESTER = env.int('CYCLE_TESTER', 20)
# definition of getter cycle, it will get proxy every CYCLE_GETTER second
CYCLE_GETTER = env.int('CYCLE_GETTER', 100)
GET_TIMEOUT = env.int('GET_TIMEOUT', 10)

# definition of tester
TEST_URL = env.str('TEST_URL', 'http://www.baidu.com')
TEST_TIMEOUT = env.int('TEST_TIMEOUT', 10)
TEST_BATCH = env.int('TEST_BATCH', 20)
# only save anonymous proxy
TEST_ANONYMOUS = env.bool('TEST_ANONYMOUS', True)
# TEST_HEADERS = env.json('TEST_HEADERS', {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
# })
TEST_VALID_STATUS = env.list('TEST_VALID_STATUS', [200, 206, 302])
# whether to set max score when one proxy is tested valid
TEST_DONT_SET_MAX_SCORE = env.bool('TEST_DONT_SET_MAX_SCORE', False)

# definition of api
API_HOST = env.str('API_HOST', '0.0.0.0')
API_PORT = env.int('API_PORT', 5555)
API_THREADED = env.bool('API_THREADED', True)
# add an api key to get proxy
# need a header of `API-KEY` in get request to pass the authenticate
# API_KEY='', do not need `API-KEY` header
API_KEY = env.str('API_KEY', '')

# flags of enable
ENABLE_TESTER = env.bool('ENABLE_TESTER', True)
ENABLE_GETTER = env.bool('ENABLE_GETTER', True)
ENABLE_SERVER = env.bool('ENABLE_SERVER', True)


ENABLE_LOG_FILE = env.bool('ENABLE_LOG_FILE', True)
ENABLE_LOG_RUNTIME_FILE = env.bool('ENABLE_LOG_RUNTIME_FILE', True)
ENABLE_LOG_ERROR_FILE = env.bool('ENABLE_LOG_ERROR_FILE', True)
