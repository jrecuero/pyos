import logging
import json
import datetime
import sys
import inspect


def _log_runner(self, attr: str):
    """log_runner adds to the logger attribute and arguments passed in any
    called method.
    """

    def _inner_log_runner(args):
        if isinstance(args, dict):
            self.dicta[attr] = args
        else:
            self.dicta[attr] = "{}".format(args)
        return self

    return _inner_log_runner


class _Formatter(logging.Formatter):
    """_Formatter class implements the functionality to format all logger
    output in JSON format.
    """

    def format(self, record):
        """format proceeds to format logging output as JSON format.
        """
        if not isinstance(record.msg, dict):
            record.msg = {record.levelname.capitalize(): record.msg}
        record.msg["timestamp"] = str(datetime.datetime.fromtimestamp(record.created))
        record.msg["logging"] = record.name
        if "file-name" not in record.msg:
            record.msg["file-name"] = record.filename
        if "lineno" not in record.msg:
            record.msg["lineno"] = record.lineno
        if "func-name" not in record.msg:
            record.msg["func-name"] = record.funcName
        return json.dumps(record.msg)


class _Logging(logging.Logger):
    """_Logging class implements a custom logging that output information in
    JSON format and it allows to define attribute/value pairs on the fly
    using method calls.
    """

    def __init__(self, *args):
        super(_Logging, self).__init__(*args)
        self.dicta = {}

    def __getattr__(self, attr):
        try:
            return self.__getattribute__(attr)
        except Exception:
            return _log_runner(self, attr)

    def call(self):
        """call should be called when implementing attribute/value pairs using
        method calls.
        """
        pframe = inspect.stack()[1]
        self.dicta["file-name"] = pframe.filename
        self.dicta["lineno"] = pframe.lineno
        self.dicta["func-name"] = pframe.function
        self.info(self.dicta)
        self.dicta = {}


loggars = {}


def get_loggar(name, handler=None):
    """get_loggar retrieves a given custom logger for the given
    module.
    """
    if name not in loggars:
        _loggar = _Logging(name)
        _fmt = _Formatter()
        if not handler:
            handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(_fmt)
        _loggar.addHandler(handler)
        loggars[name] = _loggar
    return loggars[name]


def load_loggar(filename):
    obj = []
    with open(filename, "r") as fd:
        line = fd.readline()
        while line:
            obj.append(json.loads(line))
            line = fd.readline()
    return obj


if __name__ == "__main__":

    def main():
        m.info({"fname": "jose carlos", "lname": "recuero arias"})
        m.Informato("this is informato").call()

    def insider():
        m.Insider("this is the insider").call()

    # from logging.handlers import RotatingFileHandler
    from logging import FileHandler

    # fhandler = RotatingFileHandler("loggar.log", maxBytes=(1048576 * 5), backupCount=4)
    fhandler = FileHandler("loggar.log", mode="w")
    # m = get_loggar("private-loggar")
    m = get_loggar("private-loggar", handler=fhandler)
    insider()
    m.info("logging message")
    m.debug("debug message")
    m.Info("this is an info message").call()
    m.Warmer("alarm").Info("red fire").call()
    m.Message({"data": "This is the data", "id": 100}).call()
    m.FirstName("Jose Carlos").LastName("Recuero Arias").Age(52).call()
    main()
    try:
        operation = 1 / 0
    except Exception as ex:
        m.Error(str(ex)).call()
