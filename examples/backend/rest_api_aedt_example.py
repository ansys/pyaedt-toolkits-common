from ansys.aedt.toolkits.common.backend.multithreading_server import MultithreadingServer
from ansys.aedt.toolkits.common.backend.rest_api import app
from ansys.aedt.toolkits.common.backend.rest_api import jsonify
from ansys.aedt.toolkits.common.backend.rest_api import logger
from ansys.aedt.toolkits.common.backend.rest_api import toolkit_api


# Toolkit entrypoints
@app.route("/dummy", methods=["GET"])
def get_materials():
    logger.info("[GET] /Rest API dummy call.")

    status = toolkit_api.get_thread_status()
    return jsonify(status.value), 200


if __name__ == "__main__":
    app.debug = toolkit_api.properties.debug
    server = MultithreadingServer()
    server.run(host=toolkit_api.properties.url, port=toolkit_api.properties.port, app=app)
