
from flask import Flask
from flask_caching import Cache

import conf

app = Flask(__name__)
app.config['CACHE_TYPE'] = conf.CACHE_TYPE
app.config['CACHE_REDIS_URL'] = conf.CACHE_REDIS_URL
flask_cache = Cache(app)


