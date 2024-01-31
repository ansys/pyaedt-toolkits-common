from ansys.aedt.toolkits.common.backend.multithreading_server import MultithreadingServer
from ansys.aedt.toolkits.common.backend.rest_api import app
from ansys.aedt.toolkits.common.backend.rest_api import jsonify
from ansys.aedt.toolkits.common.backend.rest_api import logger
from ansys.aedt.toolkits.common.backend.rest_api import toolkit_api


@app.route("/create_geometry", methods=["POST"])
def create_geometry():
    logger.info("[POST] /create_geometry (create a box or sphere in HFSS).")

    response = toolkit_api.create_geometry()
    if response:
        return response, 200
    else:
        return jsonify("Geometry not created"), 500


if __name__ == "__main__":
    app.debug = toolkit_api.properties.debug
    server = MultithreadingServer()
    server.run(host=toolkit_api.properties.url, port=toolkit_api.properties.port, app=app)
