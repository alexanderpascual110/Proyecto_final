from flask import Flask, render_template, request, redirect, session
from flask_mail import Mail, Message
import random

app = Flask(__name__)
app.secret_key = "clave_secreta"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "TU_CORREO@gmail.com"
app.config["MAIL_PASSWORD"] = "TU_PASSWORD_DE_APLICACION"

mail = Mail(app)

codigo_recuperacion = {}

usuarios = []
pacientes = []

# INICIO
@app.route("/")
def inicio():
    return render_template("index.html")

# REGISTRO
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        usuario = {
            "nombre": request.form["nombre"],
            "correo": request.form["correo"],
            "password": request.form["password"]
        }

        usuarios.append(usuario)

        return redirect("/login")

    return render_template("register.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        correo = request.form["correo"]
        password = request.form["password"]

        for usuario in usuarios:

            if usuario["correo"] == correo and usuario["password"] == password:

                session["usuario"] = usuario["nombre"]

                return redirect("/dashboard")

        return "Correo o contraseña incorrectos"

    return render_template("login.html")

# RECUPERAR CONTRASEÑA
@app.route("/forgot", methods=["GET", "POST"])
def forgot():

    if request.method == "POST":

        correo = request.form["correo"]

        usuario = usuarios.find_one({
            "correo": correo
        })

        if usuario:

            codigo = str(random.randint(1000, 9999))

            codigo_recuperacion[correo] = codigo

            mensaje = Message(
                "Recuperación de contraseña",
                sender=app.config["MAIL_USERNAME"],
                recipients=[correo]
            )

            mensaje.body = f"""
Hola {usuario['nombre']}

Tu código de recuperación es:

{codigo}
            """

            mail.send(mensaje)

            return redirect(f"/reset/{correo}")

        return "Correo no encontrado"

    return render_template("forgot.html")

# NUEVA CONTRASEÑA
@app.route("/reset/<correo>", methods=["GET", "POST"])
def reset(correo):

    if request.method == "POST":

        codigo = request.form["codigo"]

        nueva = request.form["password"]

        if codigo_recuperacion.get(correo) == codigo:

            usuarios.update_one(
                {"correo": correo},
                {
                    "$set": {
                        "password": nueva
                    }
                }
            )

            codigo_recuperacion.pop(correo)

            return redirect("/login")

        return "Código incorrecto"

    return render_template("reset.html", correo=correo)

# NUEVA CONTRASEÑA
@app.route("/reset/<correo>", methods=["GET", "POST"])
def reset_password(correo):

    if request.method == "POST":

        codigo = request.form["codigo"]

        nueva = request.form["password"]

        if codigo_recuperacion.get(correo) == codigo:

            usuarios.update_one(
                {"correo": correo},
                {
                    "$set": {
                        "password": nueva
                    }
                }
            )

            codigo_recuperacion.pop(correo)

            return redirect("/login")

        return "Código incorrecto"

    return render_template("reset.html", correo=correo)

# DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "usuario" in session:

        return render_template("dashboard.html", usuario=session["usuario"])

    return redirect("/login")

# PACIENTES
@app.route("/pacientes", methods=["GET", "POST"])
def pacientes_view():

    if "usuario" not in session:
        return redirect("/login")

    if request.method == "POST":

        paciente = {
            "nombre": request.form["nombre"],
            "edad": request.form["edad"],
            "enfermedad": request.form["enfermedad"],
            "telefono": request.form["telefono"]
        }

        pacientes.append(paciente)

    return render_template("pacientes.html", pacientes=pacientes)

# ELIMINAR PACIENTE
@app.route("/eliminar/<int:id>")
def eliminar(id):

    if "usuario" not in session:
        return redirect("/login")

    if id < len(pacientes):
        pacientes.pop(id)

    return redirect("/pacientes")

# CERRAR SESION
@app.route("/logout")
def logout():

    session.pop("usuario", None)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)