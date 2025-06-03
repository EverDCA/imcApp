from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from config import Config
from db import db, Usuario, IMC
from login import auth


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Manejo de login
login_manager = LoginManager()
login_manager.login_view = 'auth.login' 
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Blueprints
app.register_blueprint(auth)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/imc', methods=['GET', 'POST'])
@login_required
def index():
    imc = None
    categoria = None

    if request.method == 'POST':
        try:
            peso = float(request.form['peso'])
            altura = float(request.form['altura'])
            print(f"Peso recibido: {peso}, Altura recibida: {altura}")  # Depuración
            if peso <= 0 or altura <= 0:
                raise ValueError("Peso y altura deben ser mayores que 0.")

            altura = altura / 100  # Convertir de centímetros a metros
            imc = peso / (altura ** 2)

            if imc < 18.5:
                categoria = "Bajo peso"
            elif 18.5 <= imc < 24.999:
                categoria = "Peso normal"
            elif 25 <= imc < 29.999:
                categoria = "Sobrepeso"
            elif 30 <= imc < 34.9:
                categoria = "Obesidad I"
            elif 35 <= imc < 39.9:
                categoria = "Obesidad II"
            elif 40 <= imc < 49.9:
                categoria = "Obesidad III"
            else:
                categoria = "Obesidad IV"

            nuevo_registro = IMC(
                peso=peso,
                altura=altura,
                resultado=imc,
                categoria=categoria,
                usuario_id=current_user.id
            )
            db.session.add(nuevo_registro)
            db.session.commit()
        except (ValueError, KeyError):
            return render_template('index.html', imc=0, categoria="Error: Datos inválidos")

    return render_template('index.html', imc=imc, categoria=categoria)


@app.route('/api/imc-data', methods=['GET'])
@login_required
def get_imc_data():
    registros = IMC.query.filter_by(usuario_id=current_user.id).all()
    data = [
        {
            "id": registro.id,
            "peso": registro.peso,
            "altura": registro.altura,
            "resultado": registro.resultado,
            "categoria": registro.categoria
        }
        for registro in registros
    ]
    return jsonify(data)


@app.route('/api/imc-delete/<int:imc_id>', methods=['DELETE'])
@login_required
def delete_imc(imc_id):
    registro = IMC.query.filter_by(id=imc_id, usuario_id=current_user.id).first()
    if registro:
        db.session.delete(registro)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 404


@app.route('/api/imc-delete-all', methods=['DELETE'])
@login_required
def delete_all_imc():
    IMC.query.filter_by(usuario_id=current_user.id).delete()
    db.session.commit()
    return jsonify({"success": True})


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
