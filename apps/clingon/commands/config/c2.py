from grafo.cli import mode, STREAM


@mode("set profile")
def set(**kwargs):
    profile = kwargs.get("profile", None)

    def _exit(**kwargs):
        STREAM.out("exiting set {}".format(profile))

    STREAM.out("entering set {}".format(profile))
    return None, _exit
