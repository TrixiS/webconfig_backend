from . import web_config

__title__ = "app"
__author__ = "TrixiS"
__licence__ = "MIT"
__copyright__ = "Copyright 2021 TrixiS"
__version__ = "0.0.1"

__path__ = __import__("pkgutil").extend_path(__path__, __name__)

web_config = web_config.WebConfig()

from . import *
