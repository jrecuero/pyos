from grafo.cli import mode, command


@command("setup [name]*")
def setup(**kwargs):
    print("setup at {}".format(kwargs.get("name", None)))
    return None


@command("profile [name]+")
def profile(**kwargs):
    print("profiling with {}".format(kwargs.get("name", None)))
    return None


@mode("config")
def config(**kwargs):
    def _exit(**kwargs):
        print("exiting config")

    print("entering config...")
    return _exit


@mode("test")
def test(**kwargs):
    def _exit(**kwargs):
        print("exiting testing")

    print("entering testing...")
    return _exit
