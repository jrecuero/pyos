from grafo.cli.builder import command


@command("speed value")
def speed(**kwargs):
    val = kwargs.get("value", 0)

    def _exit():
        print("your speed was {}".format(val))

    print("set speed to {}".format(val))
    return _exit
