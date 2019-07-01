from grafo.cli import command, STREAM


@command("name fname lname")
def setup(**kwargs):
    fname = kwargs.get("fname", None)
    lname = kwargs.get("lname", None)
    STREAM.out("Your name is {} {}".format(fname, lname))
    return None, None
