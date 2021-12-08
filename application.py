import os, json
from flask import Flask, render_template, redirect, url_for, request, session, flash,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
app=Flask(__name__)

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

    #condigurar la session
app.config["SESSION_PERMANENT"]= False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
    # base de datos
engine=create_engine(os.getenv("DATABASE_URL"))
db=scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    if session.user_id: 
        return render_template("index.html")
    else:
        return render_template("layout.html")
  

@app.route("/salir")
def logout():
    session.clear()
    return redirect("register")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""                                       
    if request.method == "POST":
        # declaracion de las variables
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        #declaracion de errores
        if not request.form.get("username"):
            flash("Ingrese un nombre")
            return render_template("register.html")
        elif not request.form.get("password"):
            flash("Ingrese una contraseña")
            return render_template("register.html")
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Las contraseñas no coinciden")
            return render_template("register.html")

       #encripta la contraseña
        password = generate_password_hash(password)
        rows = db.execute("SELECT * FROM usuario WHERE username = :username",
                          {"username": username}).fetchall()

        if len(rows) != 0:
            flash("usuario existente")

        # consula la base de datos para verificar el usuario
        variable=db.execute("INSERT INTO usuario (username, password, isadmin) VALUES ( :username, :password, False)", {"username": username,"password": password})
        db.commit()
        session["user_id"]= variable
        flash("Usuario registrado")
        return redirect("/")

       

    else: 
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    #xd
    session.clear()

    # usuario es pedido por me metodo post
    if request.method == "POST":

        # usuario enviado
        if not request.form.get("username"):
            flash("Proporcione un usuario")
            return ("logint.html")

        # contraseña enviada
        elif not request.form.get("password"):
            flash("Proporcione una contraseña")
            return("login.html")

        # base de datos del usuario
        rows = db.execute("SELECT * FROM usuario WHERE username = :username",
                        username=request.form.get("username"))

        # Error si el usuario existe o la contra es incorrecta
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Contraseña o Usuario invalidos")
            return("login.html")

        # recuerda si se ha iniciado sesion previamente
        session["user_id"] = rows[0]["id"]

        # reedireccion al index
        flash("!Sesión iniciada!")
        return redirect("/")

# Mediante al get reedirige al login si no estan correctos los datos
    else:
        return render_template("login.html")

@app.route("/galeria")
def galeria():  
     return render_template("galeria")   

if __name__ == "__main__":
        app.run(port=3300,debug=True)