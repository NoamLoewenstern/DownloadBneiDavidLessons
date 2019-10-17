import logging
import sys
from os.path import join
from routes.api import api_routes

from flask import Flask, render_template, send_from_directory, jsonify, Response, abort, request, stream_with_context
from flask_cors import CORS


app = Flask(__name__, static_folder='build', template_folder='build')
app.register_blueprint(api_routes)

CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory('build', path)


@app.errorhandler(404)
def not_found(e):
    return send_from_directory(join("build", "handlers"), "404.html")


def init_logging():
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format='%(asctime)s [%(levelname)-5.5s] %(message)s',
        handlers=[
            # logging.FileHandler("{}/{}".format(log_path, log_name)),
            logging.StreamHandler()
        ]
    )


def main():
    debug = '--dev' in sys.argv
    init_logging()
    app.run(host='127.0.0.1', port=8000, debug=debug)


if __name__ == '__main__':
    main()
