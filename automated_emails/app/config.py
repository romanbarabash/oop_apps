from environs import Env

env = Env()
env.read_env(verbose=True)

USER_EMAIL = env.str('USER_EMAIL')
PASSWORD = env.str('PASSWORD')
API_KEY = env.str('API_KEY')
BASE_URL = env.str('BASE_URL')
