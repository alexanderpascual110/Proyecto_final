from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "uv_citas_secret"

# ==============================
# CONEXION MONGODB ATLAS
# ==============================

MONGO_URI = "mongodb+srv://alexanderpascual110:<alex0606>@cluster0.moyfkit.mongodb.net/?appName=Cluster0"

try:

    cliente = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000
    )

    cliente.admin.command("ping")

    print("Conectado a MongoDB Atlas")

except Exception as error:

    print("Error de conexión:", error)

# ==============================
# BASE DE DATOS
# ==============================

db = cliente["citas_medicas"]

usuarios = db["usuarios"]

pacientes = db["pacientes"]

# ==============================
# PAGINA PRINCIPAL
# ==============================

@app.route("/")
def inicio():

    return render_template("index.html")

# ==============================
# REGISTRO
# ==============================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        nuevo_usuario = {

            "nombre": request.form["nombre"],

            "correo": request.form["correo"],

            "password": request.form["password"]

        }

        usuarios.insert_one(nuevo_usuario)

        return redirect("/login")

    return render_template("register.html")

# ==============================
# LOGIN
# ==============================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        correo = request.form["correo"]

        password = request.form["password"]

        usuario = usuarios.find_one({

            "correo": correo,

            "password": password

        })

        if usuario:

            session["usuario"] = usuario["nombre"]

            return redirect("/dashboard")

        return "Correo o contraseña incorrectos"

    return render_template("login.html")

# ==============================
# DASHBOARD
# ==============================

@app.route("/dashboard")
def dashboard():

    if "usuario" not in session:

        return redirect("/login")

    return render_template(
        "dashboard.html",
        usuario=session["usuario"]
    )

# ==============================
# PACIENTES
# ==============================

@app.route("/pacientes", methods=["GET", "POST"])
def pacientes_view():

    if "usuario" not in session:

        return redirect("/login")

    if request.method == "POST":

        nuevo_paciente = {

            "nombre": request.form["nombre"],

            "edad": request.form["edad"],

            "enfermedad": request.form["enfermedad"],

            "telefono": request.form["telefono"]

        }

        pacientes.insert_one(nuevo_paciente)

    lista_pacientes = list(
        pacientes.find()
    )

    return render_template(
        "pacientes.html",
        pacientes=lista_pacientes
    )

# ==============================
# ELIMINAR PACIENTE
# ==============================

@app.route("/eliminar/<id>")
def eliminar(id):

    pacientes.delete_one({

        "_id": ObjectId(id)

    })

    return redirect("/pacientes")

# ==============================
# CERRAR SESION
# ==============================

@app.route("/logout")
def logout():

    session.pop("usuario", None)

    return redirect("/")

# ==============================
# EJECUTAR
# ==============================

if __name__ == "__main__":

    app.run(debug=True)