from grafo.cli import mode, STREAM


@mode("setup")
def setup(**kwargs):
    def _exit(**kwargs):
        STREAM.out("exiting setup")

    STREAM.out("setup roller")
    return "setup roller", _exit


@mode("play")
def profile(**kwargs):
    def _exit(**kwargs):
        STREAM.out("exiting play")

    STREAM.out("play roller")
    return "play roller", _exit
