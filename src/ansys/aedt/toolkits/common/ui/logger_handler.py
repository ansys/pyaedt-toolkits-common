import logging
import os
import tempfile

from ansys.aedt.toolkits.common.ui.properties import general_settings

debug = general_settings.debug
log_file = general_settings.log_file

# Create a logger
logger = logging.getLogger(__name__)
if debug:
    # Set log level (e.g., DEBUG, INFO, WARNING, ERROR)
    logger.setLevel(logging.DEBUG)

    # Create a file handler for the logger

    if log_file:
        temp_dir = os.path.join(tempfile.gettempdir(), log_file)
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

    # Add the console handler to the logger
    logger.addHandler(console_handler)
