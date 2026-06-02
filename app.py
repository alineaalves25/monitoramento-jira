from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def criar_tabela():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS execucoes (
            id SERIAL PRIMARY KEY,
            nome_automacao TEXT,
            escopo TEXT,
            data TEXT,
            itens_impactados TEXT,
            resultado TEXT,
            detalhes_resultado TEXT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

criar_tabela()

@app.route("/webhook", methods=["POST"])
def receber():
    dados = request.json
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO execucoes 
        (nome_automacao, escopo, data, itens_impactados, resultado, detalhes_resultado)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        dados.get("Nome_Automacao", ""),
        dados.get("Escopo", ""),
        dados.get("Data", ""),
        dados.get("Itens_Impactados", ""),
        dados.get("Resultado", ""),
        dados.get("Detalhes_Resultado", "")
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "ok"})

@app.route("/dados", methods=["GET"])
def ver_dados():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM execucoes ORDER BY id DESC")
    colunas = [desc[0] for desc in cur.description]
    registros = [dict(zip(colunas, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(registros)

@app.route("/", methods=["GET"])
def home():
    return "Monitoramento Jira - Online com PostgreSQL!"
