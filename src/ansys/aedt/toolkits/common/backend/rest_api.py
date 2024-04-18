# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from enum import Enum

from flask import Flask
from flask import jsonify
from flask import request

from ansys.aedt.toolkits.common.backend.logger_handler import logger
from ansys.aedt.toolkits.common.utils import ToolkitThreadStatus


class BodyErrorMessage(str, Enum):
    """Raises the body error message."""

    EMPTY = "Body is empty."
    INCORRECT_CONTENT = "Body content is not correct."


try:  # pragma: no cover
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
    else:  # pragma: no cover
        return jsonify(status.value), 500


@app.route("/wait_thread", methods=["GET"])
def wait_thread():
    logger.info("[GET] /wait_thread (wait until the thread is idle).")

    body = request.data
    if not body:
        msg = BodyErrorMessage.EMPTY.value
        logger.error(msg)
        return jsonify(msg), 500
    timeout = int(body.decode())

    response = toolkit_api.wait_to_be_idle(timeout=timeout)
    if response:
        return jsonify("Thread is idle, you can proceed"), 200
    else:  # pragma: no cover
        return jsonify(f"Timeout ({timeout} seconds) exceeded"), 500


@app.route("/properties", methods=["GET"])
def get_properties():
    logger.info("[GET] /properties (get toolkit properties).")
    response = toolkit_api.get_properties()
    return jsonify(response), 200


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
    response = toolkit_api.installed_aedt_version()
    return jsonify(response), 200


@app.route("/aedt_sessions", methods=["GET"])
def aedt_sessions():
    logger.info("[GET] /aedt_sessions (aedt sessions for specific version).")
    response = toolkit_api.aedt_sessions()
    if isinstance(response, dict):
        return jsonify(response), 200
    else:  # pragma: no cover
        return jsonify(response), 500


@app.route("/launch_aedt", methods=["POST"])
def launch_aedt():
    logger.info("[POST] /launch_aedt (launch or connect AEDT).")

    response = toolkit_api.launch_thread(toolkit_api.launch_aedt)
    if response:
        return jsonify("AEDT properties loaded"), 200
    else:  # pragma: no cover
        return jsonify("Fail to launch to AEDT"), 500


@app.route("/get_aedt_model", methods=["GET"])
def get_aedt_model():
    logger.info("[GET] /get_aedt_model (Get 3D model in AEDT)")

    body = request.json

    # Default values
    default_values = {
        "obj_list": None,
        "export_path": None,
        "export_as_single_objects": True,
        "air_objects": False,
        "encode": True,
    }

    # Extract values from the request body
    params = {key: body.get(key, default_values[key]) for key in default_values}

    response = toolkit_api.export_aedt_model(**params)

    if response:  # pragma: no cover
        return jsonify(response), 200
    else:
        return jsonify("No model exported"), 500


@app.route("/open_project", methods=["POST"])
def open_project():
    logger.info("[POST] /open_project (open AEDT project).")
    body = request.data

    if not body:
        msg = BodyErrorMessage.EMPTY.value
        logger.error(msg)
        return jsonify(msg), 500

    project_path = body.decode("utf-8")
    # project_path = json.loads(data)
    response = toolkit_api.open_project(project_path)

    if response:
        return jsonify("Project opened"), 200
    else:  # pragma: no cover
        return jsonify("Fail to open project"), 500


@app.route("/close_aedt", methods=["POST"])
def close_aedt():
    logger.info("[POST] /close_aedt (close AEDT).")

    body = request.json
    aedt_keys = ["close_projects", "close_on_exit"]
    if not body:
        msg = BodyErrorMessage.EMPTY.value
        logger.error(msg)
        return jsonify(msg), 500
    elif not isinstance(body, dict) or not all(item in body for item in aedt_keys):
        msg = BodyErrorMessage.INCORRECT_CONTENT.value
        logger.error(msg)
        return jsonify(msg), 500

    close_projects = body["close_projects"]
    close_on_exit = body["close_on_exit"]
    response = toolkit_api.release_aedt(close_projects, close_on_exit)

    if response:
        return jsonify("AEDT correctly released"), 200
    else:  # pragma: no cover
        return jsonify("AEDT is not connected"), 500


@app.route("/connect_design", methods=["POST"])
def connect_design():
    logger.info("[POST] /connect_design (connect or create a design).")

    body = request.json
    if not body:
        msg = BodyErrorMessage.EMPTY.value
        logger.error(msg)
        return jsonify(msg), 500

    response = toolkit_api.connect_design(body["aedtapp"])
    if response:
        return jsonify("Design connected"), 200
    else:  # pragma: no cover
        return jsonify("Fail to connect to the design"), 500


@app.route("/save_project", methods=["POST"])
def save_project():
    logger.info("[POST] /save_project (Save AEDT project).")

    body = request.json
    if not body:
        msg = BodyErrorMessage.EMPTY.value
        logger.error(msg)
        return jsonify(msg), 500

    response = toolkit_api.save_project(body)
    if response:
        return jsonify("Project saved: {}".format(body)), 200
    else:  # pragma: no cover
        return jsonify(response), 500


@app.route("/design_names", methods=["GET"])
def get_design_names():
    logger.info("[GET] /design_names (aedt designs for specific project).")
    response = toolkit_api.get_design_names()
    if isinstance(response, list):
        return jsonify(response), 200
    else:  # pragma: no cover
        return jsonify(response), 500


# Uncomment to test rest api

# if __name__ == "__main__":
#     app.debug = True
#     server = MultithreadingServer()
#     server.run(host=toolkit_api.properties.url, port=toolkit_api.properties.port, app=app)
