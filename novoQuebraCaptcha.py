import base64
import time
from io import BytesIO

from PIL import Image
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurações
URL = 'https://solucoes.receita.fazenda.gov.br/servicos/cnpjreva/cnpjreva_solicitacao.asp'
# DRIVER_PATH = '/caminho/para/seu/chromedriver'  # Altere para seu caminho
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Altere se necessário

# Configurar o Tesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def processar_captcha(imagem):
    """Processa a imagem do CAPTCHA para tentar melhorar o OCR"""
    img = imagem.convert('L')  # Converter para escala de cinza
    img = img.point(lambda x: 255 if x > 128 else 0)  # Binarização
    return img

def resolver_captcha(driver):
    # Localizar elemento do CAPTCHA
    elemento_captcha = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'imgCaptcha'))
    )
    
    # Extrair imagem do CAPTCHA (formato base64)
    img_captcha_base64 = driver.execute_script("""
        var canvas = document.createElement('canvas');
        var ctx = canvas.getContext('2d');
        var img = document.getElementById('imgCaptcha');
        canvas.height = img.naturalHeight;
        canvas.width = img.naturalWidth;
        ctx.drawImage(img, 0, 0);
        return canvas.toDataURL('image/png').substring(22);    
    """)
    
    # Decodificar imagem
    img_bytes = base64.b64decode(img_captcha_base64)
    img = Image.open(BytesIO(img_bytes))
    
    # Processar e tentar ler o CAPTCHA
    img_processada = processar_captcha(img)
    texto = pytesseract.image_to_string(img_processada).strip()
    
    return texto

def main():
    # Configurar o driver
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(URL)
        
        # Resolver CAPTCHA
        tentativas = 0
        while tentativas < 3:
            texto_captcha = resolver_captcha(driver)
            
            if not texto_captcha or len(texto_captcha) != 6:  # CAPTCHAs geralmente tem 6 caracteres
                tentativas += 1
                driver.refresh()
                time.sleep(2)
                continue
            
            # Preencher campo do CAPTCHA
            campo = driver.find_element(By.ID, 'txtTexto_captcha_serpro_gov_br')
            campo.clear()
            campo.send_keys(texto_captcha)
            
            # Tentar enviar (você precisará completar o formulário)
            # driver.find_element(...).click()
            
            # Verificar se foi bem sucedido (implementar lógica de verificação)
            break
            
    finally:
        driver.quit()

if __name__ == '__main__':
    main()