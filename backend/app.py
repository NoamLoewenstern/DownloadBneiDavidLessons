import logging
import sys
from os.path import join, realpath, dirname, isfile
from flask import (
    Flask,
    render_template,
    send_from_directory,
    jsonify,
    Response,
    abort,
    request,
    stream_with_context,
)
from flask_cors import CORS
from routes.api import api_routes


SCRIPT_DIR = (dirname(realpath(__file__)))
BUILD_PATH = realpath(join(SCRIPT_DIR, '..', 'frontend', 'build'))
print(f'BUILD_PATH: {BUILD_PATH}')

app = Flask(
    __name__,
    static_folder=join(BUILD_PATH, 'static'),
    template_folder=BUILD_PATH,
)
app.register_blueprint(api_routes)
CORS(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", defaults={"filename": ""})
@app.route("/<string:filename>")
def catch_all(filename):
    if not isfile(join(BUILD_PATH, filename)):
        return not_found(None)
    return send_from_directory(BUILD_PATH, filename)


@app.errorhandler(404)
def not_found(e):
    return send_from_directory(join(BUILD_PATH, "handlers"), "404.html")


def init_logging():
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s [%(levelname)-5.5s] %(message)s",
        handlers=[
            # logging.FileHandler(f"{log_path}/{log_name}"),
            logging.StreamHandler()
        ],
    )


def main():
    debug = "--dev" in sys.argv
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=debug)


init_logging()

if __name__ == "__main__":
    main()
