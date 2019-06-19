from grafo.cli import command


@command("set profile")
def set(**kwargs):
    profile = kwargs.get("profile", None)

    def _exit():
        print("exit set {}".format(profile))

    print("enter set {}".format(profile))
    return _exit
