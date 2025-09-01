import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ARQUIVO_JSON = 'horarios.json'

# Carrega os horários salvos do arquivo (como dicionário com chave 'horarios')
def carregar_horarios():
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, 'r') as file:
            return json.load(file)
    return {"horarios": []}  # retorna estrutura padrão se arquivo não existe

# Salva os horários no arquivo JSON (como dicionário com chave 'horarios')
def salvar_horarios(dados):
    with open(ARQUIVO_JSON, 'w') as file:
        json.dump(dados, file, indent=4)

# Rota para gerenciar os horários
@app.route('/horarios', methods=['GET', 'POST'])
def gerenciar_horarios():
    if request.method == 'GET':
        dados = carregar_horarios()
        return jsonify({'horarios': dados.get('horarios', [])})

    data = request.get_json()
    hora = data.get('hora')
    if not hora or not isinstance(hora, str):
        return jsonify({'erro': 'Horário inválido'}), 400

    dados = carregar_horarios()

 
    if 'horarios' not in dados:
        dados['horarios'] = []

  
    dados['horarios'].append(hora)
    salvar_horarios(dados)
    print(f"[NOVO] Horário adicionado: {hora}")
    return jsonify({'mensagem': 'Horário adicionado com sucesso!'}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
