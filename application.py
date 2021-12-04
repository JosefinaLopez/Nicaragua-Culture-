from flask import Flask, render_template, redirect, url_for, request, session, flash
import psycopg2 #pip install psycopg2
import psycopg2.extras
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/home")
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/salir")
def logout():
    session.clear()
    return redirect("register")


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        # ASEGURAR ENVIO DEL USER
        if not request.form.get("username"):
            flash("Ingrese un nombre")
            return render_template("register.html")
        elif not request.form.get("password"):
            flash("Ingrese una contraseña")
            return render_template("register.html")
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Las contraseñas no coinciden")
            return render_template("register.html")


        # GUARDAR DATOS
        user = request.form.get("username")
        passw = request.form.get("password")
        # REGISTRAR NUEVO USUARIO

        result = db.execute("INSERT INTO users (username,password) VALUES (:username, :password)",
                            username = user, password = generate_password_hash(passw)
                            )
        # VERIFICANDO SI EL USUARIO YA EXISTE
        if not result:
            flash("El usuario ya existe")
            return render_template("register.html")

        # ALMACENANDO EN LA SESSION
        session["user_id"] = result

        return redirect("/")
    else:
        return render_template("register.html")



@app.route("/login")
def login():
# Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash("!Sesión iniciada!")
        return redirect("/")

# User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
@app.route("/galeria")
def galeria():  
     return render_template("galeria")      