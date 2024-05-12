import uuid
import requests
from selenium.common import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import platform
from PIL import Image
import datetime


def configurar_navegador(username):
    print('Configurando o navegador')

    # Determinar o sistema operacional
    sistema_operacional = platform.system()

    # Configurar o diretório de perfil com base no sistema operacional
    if sistema_operacional == 'Windows':
        print('Windows')
        user_directory = os.path.expanduser("~")
        profile_directory = os.path.join(user_directory, "AppData", "Local", "Microsoft", "Edge", "User Data",
                                         f"Profile_{username}")
        # Configurar as opções do Navegador para o Edge no Windows
        edge_options = webdriver.EdgeOptions()
        edge_options.add_argument('--headless=new')  # Adicionar modo headless
        edge_options.add_argument('--disable-gpu')  # Desabilitar GPU para evitar problemas em ambientes headless
        edge_options.add_argument('--window-size=1920x1080')
        edge_options.add_argument(f"user-data-dir={profile_directory}")
        browser = webdriver.Edge(options=edge_options)

    elif sistema_operacional == 'Linux':
        print('Linux')

        # Configurar as opções do Navegador para o Firefox no Linux
        firefox_options = Options()
        firefox_options.add_argument("--headless")  # Executar em modo headless, sem interface gráfica
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")

        # Determinar o diretório do perfil do usuário
        #user_directory = os.path.expanduser("~")
        #profile_directory = os.path.join(user_directory, ".mozilla", "firefox", f"{username}.default-release")

        # Definir o diretório do perfil do Firefox
        #firefox_options.set_preference("profile", profile_directory)

        # Instanciar o driver do Firefox
        #browser = webdriver.Firefox(executable_path=geckodriver_path, options=firefox_options)
        browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)
        print('Configuracoes aplicadas')
    else:
        raise ValueError(f"Sistema operacional não suportado: {sistema_operacional}")

    return browser


def tirar_screenshot_qr_code(driver, nome_arquivo, tempo_espera=20):
    while len(driver.find_elements(By.ID, "side")) < 1:
        time.sleep(1)
        try:
            # Aguarde até o elemento estar presente na página
            wait = WebDriverWait(driver, tempo_espera)
            elemento_qr_code = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id=\"app\"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas")))

            print('Obtendo dimensões do QR code')
            # Obtenha a posição e dimensões do elemento que contém o QR code
            posicao_x = elemento_qr_code.location['x']
            posicao_y = elemento_qr_code.location['y']
            largura = elemento_qr_code.size['width']
            altura = elemento_qr_code.size['height']

            print('Obtendo dimensõe da janela')
            # Obtenha a largura e altura da janela do navegador
            largura_janela = driver.execute_script("return window.innerWidth")
            altura_janela = driver.execute_script("return window.innerHeight")

            print('Calculando coordenadas do objeto')
            # Calcule as coordenadas corretas para a região do elemento
            x_final = min(posicao_x + largura, largura_janela)
            y_final = min(posicao_y + altura, altura_janela)

            print('Screenshot da pagina')
            # Tire um screenshot da página inteira
            driver.save_screenshot("static/qrcodes/screenshot_qr_code.png")

            print('Abrindo Imagem')
            # Abra o screenshot como uma imagem usando a biblioteca Pillow
            imagem = Image.open("static/qrcodes/screenshot_qr_code.png")

            print('Cortando Imagem')
            # Corte a imagem para obter apenas a região desejada
            regiao_elemento = imagem.crop((posicao_x, posicao_y, x_final, y_final))

            print('Salvando...')
            # Salve o screenshot da região do elemento
            regiao_elemento.save(f"static/qrcodes/{nome_arquivo}")
            print(f'Salvo qrcode: {nome_arquivo}')

        except Exception as e:
            print("Erro geral:", str(e))

    # Remover o arquivo do QR code após o loop
    print('Excluindo...')
    os.remove(f"static/qrcodes/{nome_arquivo}")
    print(f'Removido qrcode: {nome_arquivo} ')


def tirar_screenshot_foto(driver):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4())[:8]  # Gera um ID único de 8 caracteres
    nome_arquivo = f"screenshot_{timestamp}_{unique_id}.png"
    try:
        # Aguarde até o elemento estar presente na página
        #wait = WebDriverWait(driver, tempo_espera)
        elementos_foto = driver.find_elements(By.XPATH, "//img[@class='x15kfjtz x1c4vz4f x2lah0s xdl72j9 x127lhb5 x4afe7t xa3vuyk x10e4vud']")
        elemento_foto = elementos_foto[-1]
        elemento_foto.click()
        time.sleep(1)

        elemento_foto = driver.find_element(By.XPATH, "//img[@class='x6s0dn4 x78zum5 x5yr21d xl56j7k x6ikm8r x10wlt62 x1n2onr6 xh8yej3 xhtitgo _ao3e']")
        print('Obtendo dimensões da Foto')
        # Obtenha a posição e dimensões do elemento que contém o QR code
        posicao_x = elemento_foto.location['x']
        posicao_y = elemento_foto.location['y']
        largura = elemento_foto.size['width']
        altura = elemento_foto.size['height']

        print('Obtendo dimensõe da janela')
        # Obtenha a largura e altura da janela do navegador
        largura_janela = driver.execute_script("return window.innerWidth")
        altura_janela = driver.execute_script("return window.innerHeight")

        print('Calculando coordenadas do objeto')
        # Calcule as coordenadas corretas para a região do elemento
        x_final = min(posicao_x + largura, largura_janela)
        y_final = min(posicao_y + altura, altura_janela)

        print('Screenshot da pagina')
        # Tire um screenshot da página inteira
        driver.save_screenshot(f"static/fotos/{nome_arquivo}")

        print('Abrindo Imagem')
        # Abra o screenshot como uma imagem usando a biblioteca Pillow
        imagem = Image.open(f"static/fotos/{nome_arquivo}")

        print('Cortando Imagem')
        # Corte a imagem para obter apenas a região desejada
        regiao_elemento = imagem.crop((posicao_x, posicao_y, x_final, y_final))

        print('Salvando...')
        # Salve o screenshot da região do elemento
        regiao_elemento.save(f"static/fotos/{nome_arquivo}")
        print(f'Foto salva: {nome_arquivo}')

        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)

        return f"static/fotos/{nome_arquivo}"

    except Exception as e:
        print("Erro geral:", str(e))

    time.sleep(2)


def conectar_com_numero(browser, numero):
    botao_conectar = browser.find_element(
        By.XPATH, "//*[@id=\"app\"]/div/div[2]/div[3]/div[1]/div/div/div[3]/div/span")
    botao_conectar.click()

    time.sleep(2)

    campo_numero = browser.find_element(
        By.XPATH, "//*[@id=\"app\"]/div/div[2]/div[3]/div[1]/div/div[3]/div[1]/div[2]/div/div/div/form/input")

    #Lógica para substituir o texto escrito no campo_numero pelo texto da variavel numero...

    #Tirar print do elemento que mostra o código de acesso...
    codigo = browser.find_element(By.XPATH, "//*[@id=\"app\"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div")


def fechar_conversa(browser):
    browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
    browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
    print('Fechou conversa')


def enviar_resposta(browser, mensagem):
    input_box = browser.find_element(By.XPATH, "//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p")
    input_box.send_keys(mensagem + Keys.ENTER)
    print("Resposta enviada")
    time.sleep(2)


def obter_resposta_usuario(browser):
    # Verifica se há uma mensagem não lida
    if "mensagem não lida" or "unread message" in browser.page_source:
        # Pega a lista das últimas mensagens recebidas e seleciona a última
        ingoing_messages = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "message-in")))
        last_message_element = ingoing_messages[-1]

        # Verifica se há uma imagem na mensagem
        if last_message_element.find_elements(By.TAG_NAME, "img"):
            #Lógica para Baixar a imagem
            image_filename = tirar_screenshot_foto(browser)
        else:
            image_filename = None

        # Obtém o texto da última mensagem
        last_message = last_message_element.text
        print("Texto da mensagem:", last_message)

        return last_message, image_filename
    else:
        return "Sem resposta", None


def obter_resposta_bot(browser):
    # Pega a lista das ultimas mensagens recebidas e seleciona a ultima
    if EC.presence_of_all_elements_located((By.CLASS_NAME, "message-out")):
        ingoing_messages = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "message-out")))
        last_message = ingoing_messages[-1].text
        message_lines = last_message.split('\n')
        message = message_lines[0]

    else:
        message = "Sem resposta"

    return message


def obter_numero(browser):
    classe_numero = "//*[@id=\"app\"]/div/div[2]/div[5]/span/div/span/div/div/section/div[1]/div[2]/div/span/span"
    classe_perfil = "_amie"

    try:
        # Clicar no elemento de perfil
        perfil_elemento = browser.find_element(By.CLASS_NAME, classe_perfil)
        perfil_elemento.click()

        # Esperar pelo elemento de número
        wait = WebDriverWait(browser, 10)
        elemento = wait.until(EC.presence_of_element_located((By.XPATH, classe_numero)))

        # Obter o texto do elemento
        texto = elemento.text.replace('-', '').replace(' ', '')
        print(f'Número: {texto}')

        # Fechar a visualização do perfil
        browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)

        return texto
    except TimeoutException:
        print(f"Erro: Tempo limite ao esperar pelo elemento {classe_numero}")
    except ElementClickInterceptedException:
        print(f"Erro: Outro elemento interceptou o clique em {classe_perfil}")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")