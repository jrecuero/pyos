from grafo.cli import command, STREAM


@command("speed value")
def speed(**kwargs):
    value = kwargs.get("value", None)

    def _exit():
        STREAM.out("speed was set to {}".format(value))

    STREAM.out("set speed to {}".format(value))
    return None, _exit
