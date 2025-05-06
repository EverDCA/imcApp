from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/imc', methods=['GET', 'POST'])
def index():
    imc = None
    categoria = None

    if request.method == 'POST':
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        imc = peso / (altura ** 2)

        if imc < 18.5:
            categoria = "Bajo peso"
        elif 18.5 <= imc < 24.999:
            categoria = "Peso normal"
        elif 25 <= imc < 29.999:
            categoria = "Sobrepeso"
        else:
            categoria = "Obesidad"
            
    return render_template('index.html', imc=imc, categoria=categoria)

@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
