from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "clave_secreta"

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