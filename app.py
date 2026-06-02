from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

ARQUIVO = "monitoramento.csv"
COLUNAS = [
    "Nome_Automacao",
    "Escopo",
    "Data",
    "Itens_Impactados",
    "Resultado",
    "Detalhes_Resultado"
]

if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUNAS)
        writer.writeheader()

@app.route("/webhook", methods=["POST"])
def receber():
    dados = request.json
    with open(ARQUIVO, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUNAS)
        writer.writerow({
            "Nome_Automacao": dados.get("Nome_Automacao", ""),
            "Escopo": dados.get("Escopo", ""),
            "Data": dados.get("Data", ""),
            "Itens_Impactados": dados.get("Itens_Impactados", ""),
            "Resultado": dados.get("Resultado", ""),
            "Detalhes_Resultado": dados.get("Detalhes_Resultado", "")
        })
    return jsonify({"status": "ok"})

@app.route("/dados", methods=["GET"])
def ver_dados():
    if not os.path.exists(ARQUIVO):
        return jsonify([])
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return jsonify(list(reader))

@app.route("/", methods=["GET"])
def home():
    return "Monitoramento Jira - Online!"
