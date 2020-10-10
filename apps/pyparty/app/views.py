from app import app
from flask import render_template, request, redirect
from .party import party


@app.route("/")
def app_index():
    return render_template("public/index.html", game_name=party.name)


@app.route("/activate/<member>")
def activate(member):
    party.activate(member)
    return str(party.members)


@app.route("/play")
def play():
    return party.play()


@app.route("/sign-up", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        print(f"{request.form.get('player')} was selected")
        party.activate(request.form.get("player"))
        return redirect(request.url)
    return render_template("public/sign_up.html", members=party.members)
