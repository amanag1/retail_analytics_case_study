from utils.logger.config.applicationconfigreader import ApplicationConfigReader
from utils.singleton import Singleton


class ApplicationConfig(metaclass=Singleton):
    _instance = None

    def __init__(self):
        self._instance = ApplicationConfigReader()

    def get(self, key):
        return self._instance.getValue(key)
