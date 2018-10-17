import json
import os

from flask import render_template, redirect, request
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

def validate_data(data):
    """TODO: provide basic sanity checking for data"""
    pass

@app.route('/services', methods=['GET'])
def get_services():
    pass

# Pull out the service entries for a specific name
#
# Should be sorted by date
@app.route('/services/<name>', methods=['GET'])
def service_log(name):
    history = REDIS.lrange(name, 0, 20)
    app.logger.warning(history)
    # TODO return service for the item in question
    return "OK"


# Update the service with a new log.
#
# The payload should be json of something like:
#
# {"status": "ok", "msg": "....."}
#
# We should then insert a timestamp to the data before saving.
#
# <name> should be of format: "service:$somename", that lets us do a
# scan for service keys.
@app.route('/services/<name>', methods=['POST'])
def service_update(name):
    data = request.get_json(force=True)
    app.logger.warning(request)
    app.logger.warning(data)
    validate_data(data)
    REDIS.lpush(name, json.dumps(data))
    return redirect('/services/{}'.format(name))


@app.route('/readiness', methods=['GET'])
def readiness():
    app.logger.info('Checking readiness')
    REDIS.ping()
    return '{"status": "OK"}'
