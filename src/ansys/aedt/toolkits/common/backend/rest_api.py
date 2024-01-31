import json

from flask import Flask
from flask import jsonify
from flask import request

from ansys.aedt.toolkits.common.backend.api import ToolkitThreadStatus
from ansys.aedt.toolkits.common.backend.logger_handler import logger

try:
    from api import ToolkitBackend

    toolkit_api = ToolkitBackend()
except ImportError:
    from ansys.aedt.toolkits.common.backend.api import AEDTCommon

    toolkit_api = AEDTCommon()

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def get_health():
    logger.info("[GET] /health (check if the server is healthy)")
    _, msg = toolkit_api.is_aedt_connected()
    return jsonify(msg), 200


@app.route("/status", methods=["GET"])
def get_status():
    logger.info("[GET] /status (check if the thread is running).")
    status = toolkit_api.get_thread_status()
    if status in [ToolkitThreadStatus.BUSY, ToolkitThreadStatus.IDLE]:
        return jsonify(status.value), 200
    return jsonify(status.value), 500


@app.route("/wait_thread", methods=["GET"])
def wait_thread():
    logger.info("[GET] /wait_thread (wait until the thread is idle).")

    body = request.data

    if not body:
        msg = "Body is empty."
        logger.error(msg)
        return jsonify(msg), 500

    response = toolkit_api.wait_to_be_idle(int(body.decode()))

    if response:
        return jsonify("AEDT properties loaded"), 200
    else:
        return jsonify("Fail to launch to AEDT"), 500


@app.route("/properties", methods=["GET"])
def get_properties():
    logger.info("[GET] /properties (get toolkit properties).")
    return jsonify(toolkit_api.get_properties()), 200


@app.route("/properties", methods=["PUT"])
def set_properties():
    logger.info("[PUT] /properties (set toolkit properties).")
    body = request.json
    success, msg = toolkit_api.set_properties(body)
    if success:
        return jsonify(msg), 200
    else:
        return jsonify(msg), 500


@app.route("/installed_versions", methods=["GET"])
def installed_aedt_version():
    logger.info("[GET] /version (get the version)")
    return jsonify(toolkit_api.installed_aedt_version()), 200


@app.route("/aedt_sessions", methods=["GET"])
def aedt_sessions():
    logger.info("[GET] /aedt_sessions (aedt sessions for specific version).")
    response = toolkit_api.aedt_sessions()
    if isinstance(response, dict):
        return jsonify(response), 200
    else:
        return jsonify(response), 500


@app.route("/launch_aedt", methods=["POST"])
def launch_aedt():
    logger.info("[POST] /launch_aedt (launch or connect AEDT).")

    response = toolkit_api.launch_thread(toolkit_api.launch_aedt)
    if response:
        return jsonify("AEDT properties loaded"), 200
    else:
        return jsonify("Fail to launch to AEDT"), 500


@app.route("/open_project", methods=["POST"])
def open_project():
    logger.info("[POST] /open_project (open AEDT project).")
    body = request.data

    if not body:
        msg = "Body is empty."
        logger.error(msg)
        return jsonify(msg), 500

    data = body.decode("utf-8")
    project_path = json.loads(data)
    response = toolkit_api.open_project(project_path)

    if response:
        return jsonify("Project opened"), 200
    else:
        return jsonify("Fail to open project"), 500


@app.route("/close_aedt", methods=["POST"])
def close_aedt():
    logger.info("[POST] /close_aedt (close AEDT).")

    body = request.json
    aedt_keys = ["close_projects", "close_on_exit"]
    if not body:
        msg = "Body is empty."
        logger.error(msg)
        return jsonify(msg), 500
    elif not isinstance(body, dict) or not all(item in body for item in set(aedt_keys)):
        msg = "Body not correct."
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
def connect_design():
    logger.info("[POST] /connect_design (connect or create a design).")

    body = request.json

    if not body:
        msg = "Body is empty."
        logger.error(msg)
        return jsonify(msg), 500

    response = toolkit_api.connect_design(body["aedtapp"])

    if response:
        return jsonify("Design connected"), 200
    else:
        return jsonify("Fail to connect to the design"), 500


@app.route("/save_project", methods=["POST"])
def save_project():
    logger.info("[POST] /save_project (Save AEDT project).")

    body = request.json

    if not body:
        msg = "Body is empty."
        logger.error(msg)
        return jsonify(msg), 500

    response = toolkit_api.save_project(body)

    if response:
        return jsonify("Project saved: {}".format(body)), 200
    else:
        return jsonify(response), 500


@app.route("/design_names", methods=["GET"])
def get_design_names():
    logger.info("[GET] /design_names (aedt designs for specific project).")
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
