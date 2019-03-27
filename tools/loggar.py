from typing import List
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

    def __init__(self, **kwargs):
        super(_Formatter, self).__init__(**kwargs)

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


class LoggarProc:
    def __init__(self, filename: str = "loggar.log"):
        self.log_data: List[str] = []
        with open(filename, "r") as fd:
            line = fd.readline()
            while line:
                self.log_data.append(json.loads(line))
                line = fd.readline()

    def tag(self, tagname: str):
        result: List[str] = []
        for data in self.log_data:
            tagdata = data.get(tagname, None)
            if tagdata:
                result.append(tagdata)
        return "\n".join(result)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Logger tool")
    parser.add_argument("--noserver", action="store_true", help="Launch Server")
    parser.add_argument(
        "-f",
        "--filename",
        nargs="?",
        default="loggar.log",
        help="Loggar filename (default: loggar.log)",
    )
    parser.add_argument("tag", help="Tag name")
    args = parser.parse_args()
    print(LoggarProc(args.filename).tag(args.tag))
