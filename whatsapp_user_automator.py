from selenium.common import NoSuchElementException, TimeoutException, InvalidSessionIdException
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from verificador_elementos_html import encontrar_elemento_safe, encontrar_somente_elemento_safe
from selenium_utils import configurar_navegador, fechar_conversa, enviar_resposta, obter_resposta_usuario, \
    obter_numero, tirar_screenshot_qr_code
from automation_status import *
from gemini_response import gemini_response_text, gemini_response_image

bot_ativo = False
browser_ativo = False
browser = None


def configurar_navegador_gemini(username):
    print('configurando')
    # Configurações específicas para o usuário1
    browser = configurar_navegador(username)
    print('configurado OK')
    return browser


def verificar_bot_ativo():
    return bot_ativo


def desativar(username):
    status_bots = carregar_status_bots()
    print('desativando')
    global bot_ativo, browser, browser_ativo
    print('Antes de desativar: bot_ativo =', browser_ativo)
    bot_ativo = False
    browser_ativo = False
    status_bots[username]['bot_ativo'] = False
    salvar_status_bots(status_bots)

    if browser:
        browser.quit()
        browser = None
        status_bots[username]['browser'] = False
        salvar_status_bots(status_bots)
    print('Depois de desativar: bot_ativo =', bot_ativo)


def iniciar():
    username = 'gemini'
    print(username)

    # Carrega as informações do status dos bots do arquivo JSON
    status_bots = carregar_status_bots()

    global browser, bot_ativo, browser_ativo
    # Configurar o navegador apenas se não estiver configurado
    if not browser:
        try:
            browser = configurar_navegador_gemini(username)
            # bot_ativo = True
            browser_ativo = True

            print('Depois de iniciar: bot_ativo =', bot_ativo)
            browser.get("https://web.whatsapp.com/")
            print(browser)
            status_bots[username]['browser'] = True
            salvar_status_bots(status_bots)

        except Exception as e:
            # Em caso de erro, feche o navegador e ajuste as variáveis de controle
            print(f"Erro ao iniciar o usuário: {str(e)}")
            desativar(username)

    while browser_ativo:
        try:
            if browser:
                # Autenticação
                print('Verificando Autenticacao')

                qr_code_locator = "//*[@id=\"app\"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas"
                lista_conversas_locator = "side"
                campo_pais = "selectable-text"
                # time.sleep(20)
                tempo_maximo_espera = 10
                tempo_passado = 0

                # Inicialize as variáveis fora do loop
                qr_code = None
                lista_conversas = None
                print('Tirando print')
                browser.save_screenshot(f"static/qrcodes/{username}_screenshot_qr_code_regiao.png")
                print('Print Salvo')
                while (not qr_code and not lista_conversas) and tempo_passado < tempo_maximo_espera:
                    # Use as funções esperar_elemento_por_xpath e esperar_elemento_por_id
                    try:
                        qr_code = encontrar_somente_elemento_safe(browser, By.XPATH, qr_code_locator)
                        lista_conversas = encontrar_somente_elemento_safe(browser, By.ID,
                                                                          lista_conversas_locator)
                        print("Elementos encontrados.")
                        print(f"Tempo passado: {tempo_passado}, QR: {qr_code}, Lista: {lista_conversas}")
                    except:
                        time.sleep(1)
                        tempo_passado += 1
                        print("Elementos não encontrados. Aguardando...")
                        print(f"Tempo passado: {tempo_passado}, QR: {qr_code}, Lista: {lista_conversas}")

                if qr_code:
                    while len(browser.find_elements(By.ID,
                                                           "side")) < 1:  # Loop para aguardar a conexão (QR Conde) e sincronização das mensagens

                        time.sleep(1)
                        tirar_screenshot_qr_code(browser, f"{username}_screenshot_qr_code_regiao.png")
                        if EC.presence_of_element_located(
                                (By.XPATH, "//*[@id=\"app\"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas")):
                            print("QR Code")
                            # bt_conectar_numero = browser.find_element(By.CLASS_NAME, "_2rQUO")
                            # pais = encontrar_somente_elemento_safe(browser, By.CLASS_NAME, campo_pais)
                            # if pais:
                            # conectar_com_numero(browser, "+5511915813830")

                if not qr_code:
                    while len(browser.find_elements(By.ID,
                                                           "side")) < 1:  # Loop para aguardar a conexão (QR Conde) e sincronização das mensagens

                        time.sleep(1)

                print(f'{username} Autenticado!!!')
                # Ativação verdadeora do bot
                bot_ativo = True

                # Atualiza as informações do status dos bots no arquivo JSON
                status_bots[username]['bot_ativo'] = True
                salvar_status_bots(status_bots)

                browser.find_element(By.XPATH,
                                            "//*[@id=\"side\"]/div[1]/div/button").click()  # Clica no filtro de mensagens não lidas

                while len(browser.find_elements(By.XPATH,
                                                       "//*[@id=\"pane-side\"]/div[1]/div/div")) < 1:  # Loop para aguardar a conexão e sincronização das mensagens, com base no elemento de ID "side"
                    time.sleep(1)

                conversations = browser.find_elements(By.XPATH,
                                                             "//*[@id=\"pane-side\"]/div[1]/div/div")  # XPATH da lista de conversas
                # Loop para interagir com as conversas
                while bot_ativo:
                    remetente = None
                    grupo = None
                    try:
                        # Clicar no filtro de mensagens não lidas
                        filtro_nao_lidas = WebDriverWait(browser, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//*[@id='side']/div[1]/div/button")))
                        time.sleep(1)

                        print("esperando")
                        while len(browser.find_elements(By.XPATH,
                                                               "//*[@id=\"pane-side\"]/div[1]/div/div")) < 1:  # Loop para aguardar a conexão e sincronização das mensagens, com base no elemento de ID "side"
                            time.sleep(1)

                        # Obter a lista de conversas
                        conversations = WebDriverWait(browser, 10).until(
                            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='pane-side']/div[1]/div/div")))

                        if conversations:
                            print("Clicando nas conversas:")
                            for conversation in conversations:
                                try:
                                    # Clicar na conversa
                                    conversation.click()
                                    print(
                                        f"Clicou na conversa: {conversation.text}")  # Adicione instruções de impressão
                                    time.sleep(2)

                                    # Armazena o campo onde está o contato
                                    contato = encontrar_elemento_safe(browser, By.CLASS_NAME, "x1iyjqo2")

                                    if contato:
                                        print(f"Nome do Contato: {contato}")
                                    else:
                                        print(
                                            "Nome do Contato não encontrado. Verifique o seletor ou atualize o código.")
                                    time.sleep(2)

                                    last_message, image = obter_resposta_usuario(browser)

                                    # Separar a mensagem e o horário
                                    message_lines = last_message.split('\n')

                                    if len(message_lines) == 3:
                                        grupo = contato
                                        remetente = message_lines[0]
                                        message = message_lines[1]
                                        timestamp = message_lines[2]

                                        # Imprimir as informações formatadas
                                        print("Grupo:", grupo)
                                        print("Remetente:", remetente)
                                        print("Mensagem:", message)
                                        print("Hora:", timestamp)

                                        if image:
                                            print(f"Tem imagem: {image}")
                                            enviar_resposta(browser,
                                                            gemini_response_image(message, image))
                                            fechar_conversa(browser)
                                        else:
                                            enviar_resposta(browser,
                                                            gemini_response_text(message))
                                            fechar_conversa(browser)

                                    elif len(message_lines) == 2:
                                        remetente = contato
                                        message = message_lines[0]
                                        timestamp = message_lines[1]

                                        # Imprimir as informações formatadas
                                        print("Remetente:", contato)
                                        print("Mensagem:", message)
                                        print("Hora:", timestamp)

                                        message = message.replace(' ', '')
                                        numero = obter_numero(browser)

                                        if image:
                                            print(f"Tem imagem: {image}")
                                            enviar_resposta(browser,
                                                            gemini_response_image(message, image))
                                            fechar_conversa(browser)
                                        else:
                                            enviar_resposta(browser,
                                                            gemini_response_text(message))
                                            fechar_conversa(browser)
                                    else:
                                        print("Sem mensagens")
                                        fechar_conversa(browser)

                                    time.sleep(5)

                                except TimeoutException:
                                    print(f"Elemento não encontrado:")

                                except NoSuchElementException as e:
                                    # Trate a exceção específica que ocorre quando um elemento não é encontrado
                                    print("Elemento não encontrado:", str(e))
                                    continue  # Continue para a próxima conversa

                                except InvalidSessionIdException:
                                    print('Sessão selenium inválida')
                                    continue

                                except Exception as e:
                                    print(f"Erro durante a interação com a conversa:, {str(e)}")
                                    fechar_conversa(browser)

                        else:
                            print("Não há conversas não lidas.")
                            continue
                    except Exception as e:
                        print("Erro geral:", str(e))
                        desativar(username)

        except Exception as e:
            print("Erro geral:", str(e))
            desativar(username)
        finally:
            desativar(username)
