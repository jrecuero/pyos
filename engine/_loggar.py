from logging import FileHandler
from tools.loggar import get_loggar

log = get_loggar("engine", handler=FileHandler("loggar.log", mode="w"))
