import json
import os

from flask import render_template
import redis

from status_page import app

REDIS_HOST = os.environ.get('REDIS_HOST', "localhost")
REDIS_PORT = os.environ.get('REDIS_PORT', "6379")
REDIS_PASS = os.environ.get('REDIS_PASS', "")

REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS)

@app.route('/')
def index():
    services = REDIS.scan(0, "service:*")
    app.logger.warning("services: {}".format(services))
    status = []
    for service in services[1]:
        sdata = REDIS.lrange(service, 0, 0)[0]
        app.logger.warning(sdata)
        status.append(json.loads(sdata))

    app.logger.warning(status)
    app.logger.warning('sample message')
    return render_template('index.html', podname=os.environ.get('HOSTNAME'))

# r.lpush("service:mailserver", json.dumps({"status": "warn", "msg": "over 1000 items in a delayed state"}))
#
#
#

@app.route('/readiness')
def readiness():
    app.logger.info('Checking readiness')
    REDIS.ping()
    return '{"status": "OK"}'
