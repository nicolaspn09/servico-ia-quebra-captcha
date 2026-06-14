from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta
from selenium.webdriver.chrome.options import Options
from twocaptcha import TwoCaptcha
import time 


api_key = 'REMOVED_FOR_GITHUB'
solver = TwoCaptcha(api_key)

driver = uc.Chrome()

# Defines autodownload and download PATH
params = {
    "behavior": "allow",
    "downloadPath": "G:\Meu Drive\Python RPA\RPA - Aviso de Limite - Cartão Combustível\downloads"
}
driver.execute_cdp_cmd("Page.setDownloadBehavior", params)

time.sleep(4)

driver.get(site)



# Funções para calcular datas
def agora():
    hoje = datetime.now().date()
    return hoje.strftime("%d/%m/%Y")

def dois_dias_atras():
    data_anterior = datetime.now().date() - timedelta(days=2)
    return data_anterior.strftime("%d/%m/%Y")

def ontem():
    diaAnterior = datetime.now().date() - timedelta(days=1)
    return diaAnterior.strftime("%d/%m/%Y")

antesDeOntem = dois_dias_atras()
ontem = ontem()



login = "11067623981"
senha = 'REMOVED_FOR_GITHUB'



# Espera e encontra o campo de usuário e senha, depois faz login
username_field = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cpf-input"]')))
username_field.send_keys(login)

senha_field = driver.find_element('xpath', '//*[@id="password-input"]')
senha_field.send_keys(senha)



time.sleep(3)

def quebraCaptcha():
    import os
    import sys
    from twocaptcha import TwoCaptcha


    api = 'aaf0b4fc2e71b339322b9235bf177a76'

    solver = TwoCaptcha(api)

    try:
        print("Iniciando o Captcha")

        result = solver.recaptcha(
            sitekey='6LfYr6EaAAAAAOC-4LqRuhldcp_wpNMtm1rXtcp_',
            url='https://www.aleloauto.com.br/login')
        
        return result 


        

    except Exception as e:
       # sys.exit(e)
        print(f"Erro: {e}")
    else:
        sys.exit('solved: ' + str(result['code']))

result = quebraCaptcha()
code_captcha = result['code']
driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML = '{code_captcha}'")

time.sleep(3)


# Aguarde até que o botão esteja disponível (pode precisar ajustar o tempo conforme necessário)
button = driver.find_element(By.ID, 'enter-button')

# Desative o atributo 'disabled' usando JavaScript
driver.execute_script("arguments[0].disabled = false;", button)

time.sleep(5)



elemento_login = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="enter-button"]')))
elemento_login.click()

time.sleep(3)