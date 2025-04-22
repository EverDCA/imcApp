document.getElementById('imcForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const peso = parseFloat(document.getElementById('peso').value);
    const altura = parseFloat(document.getElementById('altura').value);

    if (peso > 0 && altura > 0) {
        const imc = peso / (altura * altura);
        let mensaje = `Tu IMC es: ${imc.toFixed(1)} - `;

        if (imc < 18.5) {
            mensaje += "Bajo peso";
        } else if (imc >= 18.5 && imc < 24.9) {
            mensaje += "Peso normal";
        } else if (imc >= 25 && imc < 29.9) {
            mensaje += "Sobrepeso";
        } else {
            mensaje += "Obesidad";
        }

        document.getElementById('resultado').textContent = mensaje;
    } else {
        document.getElementById('resultado').textContent = "Por favor, introduce valores válidos.";
    }
});