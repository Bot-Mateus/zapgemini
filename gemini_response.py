import PIL.Image
import google.generativeai as genai
from selenium.webdriver import Keys

GOOGLE_API_KEY = "AIzaSyD6ikvy1UXxnWqSjV3XEsv9V5gOcGnxywo"
genai.configure(api_key=GOOGLE_API_KEY)


def break_line(message):
    br = Keys.SHIFT + Keys.ENTER + Keys.SHIFT
    message = message.replace("\n",br)
    return message


def gemini_response_text(mesage):
    generation_config = {
        "candidate_count": 1,
        "temperature": 1,
    }

    safety_settings = {
        'HATE': 'BLOCK_NONE',
        'HARASSMENT': 'BLOCK_NONE',
        'SEXUAL': 'BLOCK_NONE',
        'DANGEROUS': 'BLOCK_NONE'
    }

    model = genai.GenerativeModel(model_name='gemini-1.0-pro',
                                  generation_config=generation_config,
                                  safety_settings=safety_settings, )

    chat = model.start_chat(history=[])

    response = chat.send_message(mesage)

    return break_line(response.text)


def gemini_response_image(mesage, image):
    img = PIL.Image.open(image)

    generation_config = {
        "candidate_count": 1,
        "temperature": 0.5,
    }

    safety_settings = {
        'HATE': 'BLOCK_NONE',
        'HARASSMENT': 'BLOCK_NONE',
        'SEXUAL': 'BLOCK_NONE',
        'DANGEROUS': 'BLOCK_NONE'
    }

    model = genai.GenerativeModel(model_name='gemini-pro-vision',
                                  generation_config=generation_config,
                                  safety_settings=safety_settings, )

    response = model.generate_content([mesage, img])
    response.resolve()

    #mesage_gemini = response.text
    #mesage_gemini = break_line(mesage_gemini)

    return break_line(response.text)


#for m in genai.list_models():
  #if 'generateContent' in m.supported_generation_methods:
    #print(m.name)

# Testes com mensagem
#mesage = 'em uma frase, explique como um computador funciona para uma criança.'
#print(f'\nResposta:\n\n{gemini_response_text(mesage)}')
#mesage = 'Certo, que tal uma explicação mais detalhada para um estudante do ensino médio?'
#print(f'\nResposta:\n\n{gemini_response_text(mesage)}')

# Testes com imagem
#mesage = "Descreva em poucas palavras essa foto"
#image = "static/fotos/PXL_20220918_151756358.jpg"
#print(f'\nResposta:\n\n{gemini_response_image(mesage, image)}')


