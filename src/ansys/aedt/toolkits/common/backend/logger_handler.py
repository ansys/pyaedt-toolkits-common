import logging
import os.path
import tempfile

from ansys.aedt.toolkits.common.backend.models import common_properties

debug = common_properties.debug
log_file = common_properties.log_file

# Create a logger
logger = logging.getLogger(__name__)

if debug:
    # Set log level (e.g., DEBUG, INFO, WARNING, ERROR)
    logger.setLevel(logging.DEBUG)

    # Create a file handler for the logger
    if log_file:
        toolkit_name = common_properties.toolkit_name
        log_file_name = toolkit_name + "_" + log_file
        temp_dir = os.path.join(tempfile.gettempdir(), log_file_name)

        if not os.path.exists(temp_dir):
            file = open(temp_dir, "w")
            file.close()

        log_file = temp_dir

        file_handler = logging.FileHandler(log_file)

        # Set the log format
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)

    # Create a stream handler for logging to the console
    console_handler = logging.StreamHandler()

    # Set the log format
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)
