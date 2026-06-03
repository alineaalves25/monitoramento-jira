from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
    return conn

@app.route('/webhook', methods=['POST'])
def webhook():
    dados = request.json
    nome = dados.get('Nome_Automacao', '')
    escopo = dados.get('Escopo', '')
    data = dados.get('Data', '')
    itens = dados.get('Itens_Impactados', '')
    resultado = dados.get('Resultado', '')
    detalhes = dados.get('Detalhes_Resultado', '')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO execucoes (nome_automacao, escopo, data, itens_impactados, resultado, detalhes_resultado)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nome, escopo, data, itens, resultado, detalhes))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "ok"}), 200

@app.route('/dados', methods=['GET'])
def dados():
    senha = request.args.get('senha')
    if senha != os.environ.get('SENHA_DADOS'):
        return jsonify({"erro": "Senha incorreta"}), 401

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM execucoes ORDER BY id DESC")
    registros = cur.fetchall()
    cur.close()
    conn.close()

    resultado = []
    for r in registros:
        resultado.append({
            "id": r[0],
            "nome_automacao": r[1],
            "escopo": r[2],
            "data": r[3],
            "itens_impactados": r[4],
            "resultado": r[5],
            "detalhes_resultado": r[6]
        })

    return jsonify(resultado)

@app.route('/limpar', methods=['GET'])
def limpar():
    senha = request.args.get('senha')
    if senha != os.environ.get('SENHA_DADOS'):
        return jsonify({"erro": "Senha incorreta"}), 401

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE execucoes RESTART IDENTITY")
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensagem": "Dados apagados e ID resetado!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
