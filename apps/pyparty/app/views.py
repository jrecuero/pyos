from app import app
from party import party


@app.route("/")
def app_index():
    return "Hello world"


@app.route("/activate/<member>")
def activate(member):
    party.activate(member)
    return str(party.members)


@app.route("/play")
def play():
    return party.play()
