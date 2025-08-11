from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super_secret_key"

# ------------------ DATE LOGARE ------------------
utilizatori = [
    {"username": "Denis", "email": "Denis@test.com", "password": "admin", "rol": "admin"},
    {"username": "Alex", "email": "Alex@test.com", "password": "user", "rol": "user"},
    {"username": "Maria", "email": "Maria@test.com", "password": "admin1234", "rol": "admin"}
]


evenimente = [
    {
        "id": 1,
        "titlu": "Hackaton 2025",
        "organizator": "Denis",
        "locatie": "Cluj",
        "data": "2025-08-10",
        "locuri_disponibile": 50,
        "poza": "hhttps://t2informatik.de/en/wp-content/uploads/sites/2/2025/03/hackathon.jpg",
        "rezervari": ["alex", "johny"],
        "descriere": "Hackaton 2025 este locul unde inovatorii, programatorii si designerii se reunesc pentru a crea solutii tehnologice inedite. Evenimentul promoveaza colaborarea, creativitatea si spiritul competitiv."
    },
    {
        "id": 2,
        "titlu": "Vara pe Plaja",
        "organizator": "Denis",
        "locatie": "Bucuresti",
        "data": "2026-05-15",
        "locuri_disponibile": 50,
        "poza": "https://spotmedia.ro/wp-content/uploads/2023/08/MG0omAvLafQHfJsf_lLZiCcJnDdn6qaF.jpg",
        "rezervari": ["alex", "johny"],
        "descriere": "O experienta unica pe litoral, cu muzica live, activitati distractive si un apus spectaculos. Evenimentul promite relaxare, socializare si voie buna."
    }
]

# ------------------ LOGIN ------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        parola = request.form["password"]

        for user in utilizatori:
            if user["email"] == email and user["password"] == parola:
                session["username"] = user["username"]
                session["rol"] = user["rol"]
                flash(f"Bun venit, {user['username']}!", "success")
                return redirect(url_for("index"))

        error = "Email sau parolă incorectă."
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("rol", None)
    flash("Te-ai delogat cu succes.", "info")
    return redirect(url_for("login"))

# ------------------ LISTA EVENIMENTE (INDEX) ------------------
@app.route("/")
def index():
    locatie = request.args.get("locatie")
    data_filtru = request.args.get("data")
    sortare = request.args.get("sortare")

    lista = evenimente

    if locatie:
        lista = [e for e in lista if e["locatie"].lower() == locatie.lower()]
    if data_filtru:
        lista = [e for e in lista if e["data"] == data_filtru]

    if sortare == "data":
        lista = sorted(lista, key=lambda x: datetime.strptime(x["data"], "%Y-%m-%d"))

    return render_template("index.html", evenimente=lista)

# ------------------ DETALII EVENIMENT ------------------
@app.route("/eveniment/<int:id>")
def detalii_eveniment(id):
    ev = next((e for e in evenimente if e["id"] == id), None)
    if ev:
        return render_template("detalii_eveniment.html", eveniment=ev)
    flash("Evenimentul nu a fost găsit.", "danger")
    return redirect(url_for("index"))

# ------------------ ADAUGARE EVENIMENT ------------------
@app.route("/adauga", methods=["GET", "POST"])
def adauga_eveniment():
    if "username" not in session:  # verificam cheia corecta
        return redirect(url_for("login"))

    if request.method == "POST":
        nou_id = max([e["id"] for e in evenimente], default=0) + 1
        eveniment = {
            "id": nou_id,
            "titlu": request.form.get("titlu"),
            "organizator": session["username"],  # luam username direct
            "locatie": request.form.get("locatie"),
            "data": request.form.get("data"),
            "locuri_disponibile": int(request.form.get("locuri_disponibile")),
            "poza": request.form.get("poza"),
            "rezervari": [],
            "descriere": request.form.get("descriere")
        }
        evenimente.append(eveniment)
        flash("Eveniment adaugat cu succes!", "success")
        return redirect(url_for("index"))

    return render_template("adauga_eveniment.html")



# ------------------ MODIFICARE EVENIMENT ------------------
@app.route("/modifica/<int:id>", methods=["GET", "POST"])
def modifica_eveniment(id):
    if "username" not in session:
        return redirect(url_for("login"))

    ev = next((e for e in evenimente if e["id"] == id), None)
    if not ev:
        flash("Evenimentul nu există!", "danger")
        return redirect(url_for("index"))

    if ev["organizator"] != session["username"]:
        flash("Nu poți modifica acest eveniment!", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        ev["titlu"] = request.form.get("titlu")
        ev["locatie"] = request.form.get("locatie")
        ev["data"] = request.form.get("data")
        ev["locuri_disponibile"] = int(request.form.get("locuri_disponibile"))
        ev["poza"] = request.form.get("poza")
        flash("Eveniment modificat cu succes!", "success")
        return redirect(url_for("index"))

    return render_template("modifica_eveniment.html", eveniment=ev)

# ------------------ STERGERE EVENIMENT ------------------
@app.route("/sterge/<int:id>")
def sterge_eveniment(id):
    if "username" not in session:
        return redirect(url_for("login"))

    global evenimente
    ev = next((e for e in evenimente if e["id"] == id), None)

    if ev and ev["organizator"] == session["username"]:
        evenimente = [e for e in evenimente if e["id"] != id]
        flash("Eveniment șters cu succes!", "info")
    else:
        flash("Nu poți șterge acest eveniment!", "danger")

    return redirect(url_for("index"))

# ------------------ REZERVARE ------------------
@app.route("/rezerva/<int:id>")
def rezerva_loc(id):
    if "username" not in session:
        return redirect(url_for("login"))

    ev = next((e for e in evenimente if e["id"] == id), None)
    if not ev:
        flash("Evenimentul nu există!", "danger")
        return redirect(url_for("index"))

    username = session["username"]

    if username in ev["rezervari"]:
        flash("Ai rezervat deja un loc la acest eveniment!", "warning")
    elif ev["locuri_disponibile"] > 0:
        ev["rezervari"].append(username)
        ev["locuri_disponibile"] -= 1
        flash("Rezervare efectuată cu succes!", "success")
    else:
        flash("Nu mai sunt locuri disponibile!", "danger")

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
