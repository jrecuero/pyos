from grafo.cli import command


@command("config")
def config(**kwargs):
    def _exit():
        print("exit config")

    print("enter config...")
    return _exit
