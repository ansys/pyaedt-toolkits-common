from ansys.aedt.toolkits.common.backend.multithreading_server import MultithreadingServer
from ansys.aedt.toolkits.common.backend.rest_api import app
from ansys.aedt.toolkits.common.backend.rest_api import jsonify
from ansys.aedt.toolkits.common.backend.rest_api import logger
from ansys.aedt.toolkits.common.backend.rest_api import toolkit_api


# Toolkit entrypoints
@app.route("/dummy", methods=["GET"])
def get_materials():
    logger.info("[GET] /Rest API dummy call.")

    exit_code, msg = toolkit_api.get_thread_status()
    if exit_code <= 0:
        return jsonify(msg), 200
    else:
        return jsonify(msg), 500


if __name__ == "__main__":
    app.debug = toolkit_api.properties.debug
    server = MultithreadingServer()
    server.run(host=toolkit_api.properties.url, port=toolkit_api.properties.port, app=app)
