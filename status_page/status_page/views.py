import json
import os
import datetime

from flask import jsonify, render_template, redirect, request
import redis
from voluptuous import Schema, MultipleInvalid, Invalid

from status_page import app

REDIS_HOST = os.environ.get('REDIS_HOST', "localhost")
REDIS_PORT = os.environ.get('REDIS_PORT', "6379")
REDIS_PASS = os.environ.get('REDIS_PASS', "")

REDIS = redis.StrictRedis(
    host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS)


@app.route('/')
def index():
    return render_template('index.html', podname=os.environ.get('HOSTNAME'))


@app.route('/details/<name>')
def details(name):
    return render_template('detail.html', name=name,
                           podname=os.environ.get('HOSTNAME'))


def validate_data(data):
    s = Schema({
        'status': str,
        'msg': str
    })
    s(data)
    """TODO: provide basic sanity checking for data"""


@app.errorhandler(MultipleInvalid)
@app.errorhandler(Invalid)
def api_error(error):
    response = jsonify({"error":
                        "Must provide a 'status' and a "
                        "'msg' which must both be strings"})
    response.status_code = 400
    return response


@app.route('/services', methods=['GET'])
def get_services():
    services = REDIS.scan(0, "service:*")
    status = []
    for service in services[1]:
        sdata = REDIS.lrange(service, 0, 0)[0]
        app.logger.warning(sdata)
        data = json.loads(sdata)
        data["name"] = service.decode('utf-8')
        status.append(data)
    rdata = {
        "podname": os.environ.get('HOSTNAME'),
        "services": status
    }
    return json.dumps(rdata)


# Pull out the service entries for a specific name
#
# Should be sorted by date
@app.route('/services/<name>', methods=['GET'])
def service_log(name):
    history = [json.loads(x) for x in REDIS.lrange(name, 0, 20)]
    app.logger.warning(history)
    # TODO return service for the item in question
    rdata = {
        "podname": os.environ.get('HOSTNAME'),
        "history": history
    }
    return json.dumps(rdata)


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
    app.logger.warning(request)
    data = request.get_json(force=True)
    app.logger.warning(request)
    app.logger.warning(data)
    validate_data(data)
    data["updated_at"] = datetime.datetime.utcnow().\
        replace(microsecond=0).isoformat()
    REDIS.lpush(name, json.dumps(data))
    return redirect('/services/{}'.format(name))


@app.route('/readiness', methods=['GET'])
def readiness():
    app.logger.info('Checking readiness')
    REDIS.ping()
    return '{"status": "OK"}'
