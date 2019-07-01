from grafo.cli import mode, STREAM


@mode("setup")
def setup(**kwargs):
    def _exit(**kwargs):
        STREAM.out("exiting setup")

    STREAM.out("setup roller")
    return None, _exit


@mode("play")
def profile(**kwargs):
    def _exit(**kwargs):
        STREAM.out("exiting play")

    STREAM.out("play roller")
    return None, _exit
