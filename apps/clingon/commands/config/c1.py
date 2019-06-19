from grafo.cli import command


@command("login hostname user")
def login(**kwargs):
    hostname = kwargs.get("hostname", None)
    user = kwargs.get("user", None)

    def _exit():
        print("{} exits {}".format(user, hostname))

    print("Login in {} as {}".format(hostname, user))
    return _exit
