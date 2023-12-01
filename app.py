from flask import Flask
from flask import request
from datetime import datetime

app = Flask(__name__)

BD = {"21345": {"nombre": "Arnaldo", "saldo": 200, "contactos": ["123", "456"]},
      "123": {"nombre": "Luisa", "saldo": 400, "contactos": ["456"]},
      "456": {"nombre": "Andrea", "saldo": 300, "contactos": ["21345"]}}

REG = []


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/billetera/contactos')
def datos_contactos():
    args = request.args
    numero = args.get("minumero")
    if numero in BD:
        contactos = BD[numero]["contactos"]
        res = {}
        for c in contactos:
            res[c] = BD[c]["nombre"]
        return res
    else:
        return {"mensaje": "Número no encontrado"}


@app.route('/billetera/pagar')
def pagar():
    args = request.args
    numero_o = args.get("minumero")
    numero_d = args.get("numerodestino")
    agregado = args.get("valor")
    if (numero_o in BD) and (numero_d in BD):
        if agregado < BD[numero_o]["saldo"]:
            BD[numero_o]["saldo"] -= agregado
            BD[numero_d]["saldo"] += agregado
            fecha = datetime.today().strftime("%Y-%m-%d")
            registro = {"numero_0": numero_o, "numero_d": numero_d, "fecha": fecha, "valor": agregado}
            REG.append(registro)
            return f"Realizado en {fecha}"
        else:
            return {"mensaje": "El valor a depositar es mayor al saldo disponible"}
    else:
        return {"mensaje": "Alguno de los números ingresados son inválidos"}


@app.route('/billetera/historial')
def ver_historial():
    args = request.args
    numero = args.get("minumero")
    if numero in BD:
        nombre = BD[numero]["nombre"]
        recibidos = {}
        for r in REG:
            if r["numero_d"] == numero:
                recibidos[BD[r["numero_o"]]["nombre"]] = r["valor"]
        dados = {}
        for r in REG:
            if r["numero_o"] == numero:
                dados[BD[r["numero_d"]]["nombre"]] = r["valor"]
        saldo = BD[numero]["saldo"]
        res = f"saldo de {nombre}: {saldo}\nOperaciones de {nombre}\n"
        for i in dados:
            res += f"Pago recibido de {dados[i]} de {i}"
        for j in recibidos:
            res += f"Pago recibido de {recibidos[j]} de {j}"
        return res
    else:
        return {"mensaje": "Número no encontrado"}


if __name__ == '__main__':
    app.run()
