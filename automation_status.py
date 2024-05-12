import json

# Caminho para o arquivo JSON que armazenará as informações do status dos bots
STATUS_FILE_PATH = 'status_bots.json'


# Função para carregar as informações do status dos bots do arquivo JSON
def carregar_status_bots():
    try:
        with open(STATUS_FILE_PATH, 'r') as status_file:
            # Tenta carregar o JSON do arquivo
            status_bots = json.load(status_file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existir ou não for um JSON válido, inicializa com um dicionário vazio
        status_bots = {}

    return status_bots


# Função para salvar as informações do status dos bots no arquivo JSON
def salvar_status_bots(status_bots):
    with open(STATUS_FILE_PATH, 'w') as status_file:
        json.dump(status_bots, status_file, indent=2)  # Adiciona indent para tornar o JSON mais legível


# Função para verificar se o bot está ativo no arquivo JSON
def verificar_bot_ativo(username):
    # Carrega as informações do status dos bots
    status_bots = carregar_status_bots()
    print('Verificando ativação')
    # Retorna True se o bot estiver ativo para o usuário específico, False caso contrário
    return status_bots.get(username, {}).get('bot_ativo', False)