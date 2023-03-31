from flask import Flask, make_response, jsonify, request
from bd import Alunos

app = Flask(__name__) # Instanciando o flask.
app.config["JSON_SORT_KEYS"] = False # Confingurando para não ordenar o jsonResponse.

# GET, CREATE
@app.route("/alunos", methods=["GET"])
def get_alunos():
    return make_response(
        jsonify(Alunos) # Retornando o jsonResponse com a configuração do flask.
    )

# POST, INSERT
@app.route("/alunos", methods=["POST"])
def insert_aluno():
    aluno = request.json # Requisição do JSON passado para a API.
    Alunos.append(aluno)
    return make_response(
        jsonify(aluno) # Retornando o jsonResponse com a configuração do flask.
    )

app.run()