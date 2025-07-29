import sys
import warnings

from examples.toolkit.pyaedt_toolkit.backend.api import ToolkitBackend

from ansys.aedt.toolkits.common.backend.multithreading_server import MultithreadingServer
from ansys.aedt.toolkits.common.backend.rest_api import app
from ansys.aedt.toolkits.common.backend.rest_api import jsonify

from ansys.aedt.toolkits.common.backend.rest_api import logger

toolkit_api = ToolkitBackend()

if len(sys.argv) == 3:
    toolkit_api.properties.url = sys.argv[1]
    toolkit_api.properties.port = int(sys.argv[2])


@app.route("/create_geometry", methods=["POST"])
def create_geometry():
    logger.info("[POST] /create_geometry (create a box or sphere in HFSS).")

    response = toolkit_api.create_geometry()
    if response:
        return response, 200
    else:
        return jsonify("Geometry not created"), 500


def run_backend(port=None):
    """Run the server."""
    app.debug = toolkit_api.properties.debug
    server = MultithreadingServer()
    if not port:
        warnings.warn("Using port value defined in toolkit properties.")
        port = toolkit_api.properties.port
    server.run(host=toolkit_api.properties.url, port=port, app=app)


if __name__ == "__main__":
    run_backend()
