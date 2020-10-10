from grafo.cli import command, STREAM


@command("name fname lname")
def setup(**kwargs):
    fname = kwargs.get("fname", None)
    lname = kwargs.get("lname", None)
    user_data = kwargs.get("__user_data__")
    fname_widget = user_data["fname"]
    lname_widget = user_data["lname"]
    STREAM.out("Your name is {} {}".format(fname, lname))
    fname_widget.set_text(fname)
    lname_widget.set_text(lname)
    return "Your name is {} {}".format(fname, lname), None
