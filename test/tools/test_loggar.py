from logging import FileHandler
from tools.loggar import get_loggar

log = get_loggar("test-loggar", handler=FileHandler("test-loggar.log", mode="w"))


if __name__ == "__main__":
    log.Test("loggar").Status("active").call()
