import json
import logging
import os
import socket
import sys
from collections import OrderedDict
from datetime import datetime

from jsonformatter import JsonFormatter

from utils.logger.config.applicationconfig import ApplicationConfig
from utils.singleton import Singleton

appConfig = ApplicationConfig()


class AppLogger(metaclass=Singleton):
    _logger = None
    _logLabelPrefix = appConfig.get('logLabelPrefix')

    def DEFAULT_SOLUTION(o):
        if not isinstance(o, (str, int, float, bool, type(None))):
            return str(o)
        else:
            return o

    class CLS_SOLUTION(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, datetime.datetime):
                return o.isoformat()
            return json.JSONEncoder.default(self, o)

    def __init__(self):

        self._logger = logging.getLogger()
        self._logger.setLevel(appConfig.get('logLevel'))

        RECORD_CUSTOM_ATTRS = {
            'asctime': lambda: datetime.today()
        }

        RECORD_CUSTOM_FORMAT = OrderedDict([
            (self._logLabelPrefix + 'asctime', "%(asctime)s"),
            (self._logLabelPrefix + 'message', "message")
        ])

        formatter = JsonFormatter(RECORD_CUSTOM_FORMAT, record_custom_attrs=RECORD_CUSTOM_ATTRS,
                                  default=self.DEFAULT_SOLUTION, cls=self.CLS_SOLUTION,
                                  ensure_ascii=True, mix_extra=True,
                                  mix_extra_position='head')  # optional: head, mix, tail)

        now = datetime.now()

        if 'logs' not in os.listdir(appConfig.get('logRoot')):
            os.mkdir(appConfig.get('logDir'))

        # The log file name includes the date added into the suffix to create new files across dates
        filehandler = logging.FileHandler(
            appConfig.get('logDir') + "/log_" + now.strftime("%Y-%m-%d") + ".log")
        filehandler.setFormatter(formatter)

        self._logger.addHandler(filehandler)

    def constructLogStatement(self, level, entry={}):

        extrasdict = {self._logLabelPrefix + 'ts': str(datetime.now().isoformat()),
                      self._logLabelPrefix + 'source': socket.gethostname(),
                      self._logLabelPrefix + 'level': level,
                      self._logLabelPrefix + 'time_millis': str(datetime.now().timestamp()),
                      self._logLabelPrefix + 'lineno': sys._getframe(2).f_lineno,
                      self._logLabelPrefix + 'filename': sys._getframe(2).f_code.co_filename,
                      self._logLabelPrefix + 'funcName': sys._getframe(2).f_code.co_name}

        # Note: sys._getframe(2). In case the hierarchy of calls is changed, this code is impacted

        # Add custom attributes received
        for key in entry:
            extrasdict[self._logLabelPrefix + key] = entry[key]

        return extrasdict

    def debug(self, message, entry={}):

        self._logger.debug(message, extra=self.constructLogStatement('debug', entry))

    def info(self, message, entry={}):

        self._logger.info(message, extra=self.constructLogStatement('info', entry))

    def warning(self, message, entry={}):

        self._logger.warning(message, extra=self.constructLogStatement('warning', entry))

    def error(self, message, entry={}):

        self._logger.error(message, exc_info=True, extra=self.constructLogStatement('error', entry))

    def critical(self, message, entry={}):

        self._logger.critical(message, extra=self.constructLogStatement('critical', entry))
