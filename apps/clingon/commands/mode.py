from grafo.cli import mode, command, STREAM


@command("setup [name]*")
def setup(**kwargs):
    STREAM.out("setup at {}".format(kwargs.get("name", None)))
    return None


@command("profile [name]+")
def profile(**kwargs):
    STREAM.out("profiling with {}".format(kwargs.get("name", None)))
    return None


@mode("config")
def config(**kwargs):
    def _exit(**kwargs):
        STREAM.out("exiting config")

    STREAM.out("entering config...")
    return None, _exit


@mode("test")
def test(**kwargs):
    def _exit(**kwargs):
        STREAM.out("exiting testing")

    STREAM.out("entering testing...")
    return None, _exit
