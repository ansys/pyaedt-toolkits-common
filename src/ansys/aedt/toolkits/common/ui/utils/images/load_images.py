import os
import pathlib

from ansys.aedt.toolkits.common.ui.logger_handler import logger
from ansys.aedt.toolkits.common.ui.models import general_settings


class LoadImages(object):
    def __init__(self, path=None):
        self.images_path = self._init_images_path(path)

    @staticmethod
    def _init_images_path(path):
        if (not path or not hasattr(general_settings, "images")) and not general_settings.images:
            return pathlib.Path(__file__).resolve().parent
        else:
            if path:
                abs_path = os.path.abspath(path)
            else:
                abs_path = general_settings.images
            if not os.path.exists(abs_path):
                msg = "{} does not exist".format(abs_path)
                logger.error(msg)
                raise FileNotFoundError(msg)
            return abs_path

    def icon_path(self, icon_name):
        return self._build_asset_path("icons", icon_name)

    def image_path(self, file_name):
        return self._build_asset_path("files", file_name)

    def _build_asset_path(self, folder, filename):
        path = os.path.join(self.images_path, folder, filename)
        if not os.path.exists(path):
            logger.error("{} does not exist".format(folder.capitalize()))
            return False
        return path
