import threading

from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from automation_status import *
from automation_status import salvar_status_bots
import time
from whatsapp_user_automator import iniciar, desativar
import json

app = Flask(__name__)


# Função para iniciar o robô em uma thread separada
def iniciar_em_thread():
    t = threading.Thread(target=iniciar)
    t.daemon = True
    t.start()


@app.route('/')
def index():
    username = 'gemini'  # Defina o valor de username aqui
    return render_template('index.html', username=username)


@app.route('/toggle_ai', methods=['POST'])
def toggle_ai():
    username = 'gemini'
    try:
        status_bots = carregar_status_bots()

        if username in status_bots and status_bots[username].get('bot_ativo', False):
            return jsonify({'status': 'error', 'message': 'O robô já está ativo!'})
        else:
            iniciar_em_thread()  # Chama a função iniciar() em uma thread separada
            status_bots.setdefault(username, {'bot_ativo': False})
            salvar_status_bots(status_bots)
            tempo_maximo_espera = 300
            tempo_passado = 0

            while not verificar_bot_ativo(username) and tempo_passado < tempo_maximo_espera:
                time.sleep(1)
                tempo_passado += 1

            if verificar_bot_ativo(username):
                status_bots[username]['bot_ativo'] = True
                salvar_status_bots(status_bots)

            return jsonify({'status': 'success', 'message': 'Robô ativado com sucesso!'})
    except Exception as e:
        print(f"Erro durante a execução da função iniciar: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro ao ativar o robô.'})


@app.route('/desativar_funcao/<username>')
def desativar_funcao(username):
    try:
        # Carrega as informações do status dos bots do arquivo JSON
        status_bots = carregar_status_bots()
        if username in status_bots and status_bots[username].get('bot_ativo', False):
            # Lógica para desativar o bot específico para o usuário
            desativar(username)

            # Atualiza as informações do status dos bots no arquivo JSON
            status_bots[username]['bot_ativo'] = False
            status_bots[username]['browser'] = None
            salvar_status_bots(status_bots)

            return jsonify({'status': 'success', 'message': 'Robô desativado com sucesso!'})
        else:
            return jsonify({'status': 'error', 'message': 'O robô já está desativado para este usuário!'})

    except Exception as e:
        print(f"Erro durante a execução da função desativar_funcao: {str(e)}")
        flash('Erro ao desativar o robô. Tente novamente.', 'error')
        return redirect(url_for('home'))


@app.route('/update_autenticacao/<username>', methods=['POST'])
def update_autenticacao(username):
    print('updating autenticacao')
    data = request.json
    autenticacao = data.get('autenticacao')  # Obter o novo valor de autenticação do JSON
    username = data.get('username')

    # Carregar informações atuais do arquivo JSON
    status_bots = carregar_status_bots()

    # Verificar se o usuário existe no status_bots
    if username in status_bots:
        # Atualizar o campo 'autenticacao' se o username existir
        status_bots[username]['autenticacao'] = autenticacao
        salvar_status_bots(status_bots)
        bot_info = status_bots[username]
        return jsonify({'message': 'Autenticação atualizada com sucesso', 'botAtivo': bot_info.get('bot_ativo', False),
                        'autenticacao': bot_info.get('autenticacao', 'QRCODE')}), 200
    else:
        return jsonify({'message': f'Usuário {username} não encontrado'}), 404


@app.route('/status_bot/<username>')
def status_bot(username):
    try:
        # Carrega as informações do status dos bots do arquivo JSON
        status_bots = carregar_status_bots()

        if username in status_bots:
            bot_info = status_bots[username]
            return jsonify({'status': 'success', 'botAtivo': bot_info.get('bot_ativo', False), 'autenticacao': bot_info.get('autenticacao', 'QRCODE')})
        else:
            return jsonify({'status': 'error', 'message': 'Usuário não autenticado ou inexistente.'})
    except Exception as e:
        print(f"Erro durante a execução da função status_bot: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Erro durante a execução da função status_bot.'})


if __name__ == '__main__':
    app.run(debug=True)
