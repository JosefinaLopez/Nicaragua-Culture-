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


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET","POST"])
def index():
    if 'username' in session:

        username = session["username"]
        id_user = db.execute("SELECT iduser FROM usuario WHERE username = :username AND isadmin=True OR isadmin=False",
                          {"username" :username}).fetchone()[0]
        publication = db.execute("SELECT titulo , shortcontent, longcontent , likes, register_date FROM publication").fetchall()                 
        return render_template("index.html", username= username, publication=publication) 
    else: 
        return render_template("login.html")
    


@app.route("/comentarios", methods=["GET","POST"])
def comentarios():
    if 'username' in session:
        #Comentarios
        comentarios= request.form.get("comentarios")
        #inserta de la tabla comentarios los sig datos 
        cm= db.execute("INSERT INTO comentarios idcomentarios, comentario, iduser,fecha  VALUES (:idcomentarios, :idpublication, :comentario,:iduser,:fecha)")
        { "idcomentarios" :idcomentarios, "comentario" :comentario, "iduser" :iduser, "fecha" :fecha}
        #envia la informacion
        db.commit() 
        #confirma 
        flash("Publicacion agregada con exito")  
        return render_template("index.html", comentarios= comentarios) 
    else: 
        return render_template("login.html")
  

@app.route("/salir")
def salir():
    session.clear()
    return render_template("login.html")

@app.route("/galery")
def galery():
    return render_template("galery.html")    


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
        rows = db.execute("SELECT * FROM usuario WHERE username = :username",
                          {"username": username}).fetchall()

        if len(rows) != 0:
            return "error"
        password = generate_password_hash(password)
        # consula la base de datos para verificar el usuario
        variable=db.execute("INSERT INTO usuario (username, password, isadmin) VALUES ( :username, :password, False)", {"username": username,"password": password})
       
        db.commit()
        session["user_id"]= rows
        flash("Usuario registrado")
        return redirect(url_for("index"))
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
            return render_template("login.html")

        # contraseña enviada
        elif not request.form.get("password"):
            flash("Proporcione una contraseña")
            return render_template("login.html")

        username = request.form.get("username")
        # base de datos del usuario
        rows = db.execute("SELECT * FROM usuario WHERE username = :username",
                          {"username": username}).fetchall()                 

        # Error si el usuario existe o la contra es incorrecta
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            flash("Contraseña o Usuario invalidos")
            return render_template("login.html")

        print(rows)
        if rows[0][3] == True:
            session["isadmin"]= rows

        # recuerda si se ha iniciado sesion previamente
        else:
            session["user_id"]= rows
        session["username"] = username
            # reedireccion al index
        flash("!Sesión iniciada!")
        return redirect(url_for("index"))

# Mediante al get reedirige al login si no estan correctos los datos
    else:
        return render_template("login.html")

@app.route("/agregar", methods=["GET", "POST"])
def agregar():  
    if request.method == "POST":
        #declaracion de variables
        titulo= request.form.get("titulo")
        shortcontent= request.form.get("shortcontent")
        longcontent= request.form.get("longcontent")
        #se obtiene session del usuario con username
        username = session.get("username")
        #se consulta en la bd el nombre y que el admin sea igual a True
        id_user = db.execute("SELECT iduser FROM usuario WHERE username = :username AND isadmin=True",
                          {"username": username}).fetchone()[0] 
        #Se hace la inserccion en la tabla de publication 
        db.execute("INSERT INTO publication(iduser,titulo,shortcontent,longcontent,likes) VALUES(:iduser, :titulo,:shortcontent,:longcontent, 0)",
                   {"iduser":id_user,"titulo" :titulo, "shortcontent":shortcontent,"longcontent" :longcontent})
        db.commit() 
        flash("Publicacion agregada con exito")  

        return redirect(url_for("index")) 
    else: 
        return render_template("publication.html")
if __name__ == "__main__":
        app.run(port=3300,debug=True)

        