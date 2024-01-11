from flask import Flask
from flask import jsonify
from flask import request

from ansys.aedt.toolkits.common.backend.api import Backend
from ansys.aedt.toolkits.common.backend.logger_handler import logger

toolkit_api = Backend()

app = Flask(__name__)


# Generic services


@app.route("/health", methods=["GET"])
def get_health():
    logger.info("[GET] /health (check if the server is healthy)")
    desktop_connected, msg = toolkit_api.aedt_connected()
    if desktop_connected:
        return jsonify(msg), 200
    else:
        return jsonify(msg), 200


@app.route("/get_status", methods=["GET"])
def get_status_call():
    logger.info("[GET] /get_status (check if the thread is running)")
    exit_code, msg = toolkit_api.get_thread_status()
    if exit_code <= 0:
        return jsonify(msg), 200
    else:
        return jsonify(msg), 500


@app.route("/get_properties", methods=["GET"])
def get_properties_call():
    logger.info("[GET] /get_properties (get toolkit properties)")
    return jsonify(toolkit_api.get_properties()), 200


@app.route("/set_properties", methods=["PUT"])
def set_properties_call():
    logger.info("[PUT] /set_properties (set toolkit properties)")

    body = request.json
    success, msg = toolkit_api.set_properties(body)
    if success:
        return jsonify(msg), 200
    else:
        return jsonify(msg), 500


@app.route("/installed_versions", methods=["GET"])
def installed_aedt_version_call():
    logger.info("[GET] /version (get the version)")
    return jsonify(toolkit_api.installed_aedt_version()), 200


@app.route("/aedt_sessions", methods=["GET"])
def aedt_sessions_call():
    logger.info("[GET] /aedt_sessions (aedt sessions for specific version)")

    response = toolkit_api.aedt_sessions()

    if isinstance(response, list):
        return jsonify(response), 200
    else:
        return jsonify(response), 500


@app.route("/launch_aedt", methods=["POST"])
def launch_aedt_call():
    logger.info("[POST] /launch_aedt (launch or connect AEDT)")

    response = toolkit_api.launch_aedt()
    if response:
        return jsonify("AEDT properties loaded"), 200
    else:
        return jsonify("Fail to launch to AEDT"), 500


@app.route("/close_aedt", methods=["POST"])
def close_aedt_call():
    logger.info("[POST] /close_aedt (close AEDT)")

    body = request.json
    aedt_keys = ["close_projects", "close_on_exit"]
    if not body:
        msg = "body is empty!"
        logger.error(msg)
        return jsonify(msg), 500
    elif not isinstance(body, dict) or not all(item in body for item in set(aedt_keys)):
        msg = "body not correct"
        logger.error(msg)
        return jsonify(msg), 500

    close_projects = body["close_projects"]
    close_on_exit = body["close_on_exit"]
    response = toolkit_api.release_aedt(close_projects, close_on_exit)

    if response:
        return jsonify("AEDT correctly released"), 200
    else:
        return jsonify("AEDT is not connected"), 500


@app.route("/connect_design", methods=["POST"])
def connect_design_call():
    logger.info("[POST] /connect_design (connect or create a design)")

    body = request.json

    if not body:
        msg = "body is empty!"
        logger.error(msg)
        return jsonify("body is empty!"), 500

    response = toolkit_api.connect_design(body["aedtapp"])

    if response:
        return jsonify("Design connected"), 200
    else:
        return jsonify("Fail to connect to the design"), 500


@app.route("/save_project", methods=["POST"])
def save_project_call():
    logger.info("[POST] /save_project (Save AEDT project)")

    body = request.json

    if not body:
        msg = "body is empty!"
        logger.error(msg)
        return jsonify("body is empty!"), 500

    response = toolkit_api.save_project(body)

    if response:
        return jsonify("Project saved: {}".format(body)), 200
    else:
        return jsonify(response), 500


@app.route("/get_design_names", methods=["GET"])
def get_design_names_call():
    logger.info("[GET] /get_design_names (aedt designs for specific project)")

    response = toolkit_api.get_design_names()

    if isinstance(response, list):
        return jsonify(response), 200
    else:
        return jsonify(response), 500

# Uncomment to test rest api

# if __name__ == "__main__":
#     app.debug = True
#     server = MultithreadingServer()
#     server.run(host=toolkit_api.properties.url, port=toolkit_api.properties.port, app=app)
