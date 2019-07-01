from grafo.cli import command, STREAM


@command("talk talkto")
def talk(**kwargs):
    talkto = kwargs.get("talkto", None)

    STREAM.out("Talk to {}".format(talkto))
    return None, None


@command("move moveto")
def move(**kwargs):
    moveto = kwargs.get("moveto", None)

    STREAM.out("Move to {}".format(moveto))
    return None, None


@command("look lookat")
def look(**kwargs):
    lookat = kwargs.get("lookat", None)

    STREAM.out("Look at {}".format(lookat))
    return None, None
