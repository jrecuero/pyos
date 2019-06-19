from grafo.cli import command


@command("speed value")
def speed(**kwargs):
    value = kwargs.get("value", None)

    def _exit():
        print("speed was set to {}".format(value))

    print("set speed to {}".format(value))
    return _exit
