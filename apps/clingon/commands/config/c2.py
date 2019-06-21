from grafo.cli import mode


@mode("set profile")
def set(**kwargs):
    profile = kwargs.get("profile", None)

    def _exit(**kwargs):
        print("exiting set {}".format(profile))

    print("entering set {}".format(profile))
    return _exit
