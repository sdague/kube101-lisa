import os
from flask import Flask

app = Flask(__name__)
app.config.from_object('status_page.default_settings')
app.debug = True

if not app.debug:
    import logging
    from logging.handlers import TimedRotatingFileHandler
    # https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
    file_handler = TimedRotatingFileHandler(
        os.path.join(app.config['LOG_DIR'], 'status_page.log'), 'midnight')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(
        logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
    app.logger.addHandler(file_handler)

import status_page.views  # noqa


def run():
    app.run(host='0.0.0.0')
