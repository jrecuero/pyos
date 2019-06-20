from grafo.cli import mode


@mode("config")
def config(**kwargs):
    def _exit():
        print("exit config")

    print("enter config...")
    return _exit


@mode("test")
def test(**kwargs):
    def _exit():
        print("exit testing")

    print("enter testing...")
    return _exit
