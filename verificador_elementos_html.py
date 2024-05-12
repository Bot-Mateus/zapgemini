from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def encontrar_elemento_safe(driver, by, value):
    try:
        elemento = WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
        return elemento.text
    except TimeoutException:
        print(f"Elemento não encontrado: {value}")
        return None


def encontrar_somente_elemento_safe(driver, by, value):
    try:
        elemento = WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
        return elemento
    except TimeoutException:
        print(f"Elemento não encontrado: {value}")
        return None