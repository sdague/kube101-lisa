from flask import render_template

from status_page import app


@app.route('/')
def index():
    app.logger.warning('sample message')
    return render_template('index.html')

@app.route('/health')
def health():
    app.logger.info('Checking health')
    return '{"status": "OK"}'
