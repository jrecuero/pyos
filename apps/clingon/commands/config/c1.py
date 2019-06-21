from grafo.cli import command, STREAM


@command("login hostname user")
def login(**kwargs):
    hostname = kwargs.get("hostname", None)
    user = kwargs.get("user", None)

    def _exit():
        STREAM.out("{} exits {}".format(user, hostname))

    STREAM.out("Login in {} as {}".format(hostname, user))
    return None, _exit
