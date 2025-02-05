import sys
import os
import django
from decimal import Decimal
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from catalogo.models import Produto  # Importe o modelo Produto

# Configuração do Selenium
url = "https://lista.mercadolivre.com.br/computador-gamer-i7-16gb-ssd-1tb"
options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(url)

# Aguarda os elementos serem carregados
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "andes-card"))
)

# Coleta os elementos dos produtos
product_elements = driver.find_elements(By.CLASS_NAME, "andes-card")

for index, product in enumerate(product_elements, start=1):
    if index == 1:
        continue  # Pula o primeiro produto (pode ser um anúncio)

    if index > 5:
        break  # Limita a coleta a 50 produtos

    print("-" * 80)

    # Coleta dos dados
    try:
        link_element = product.find_element(By.CLASS_NAME, "poly-component__title")
        link = link_element.get_attribute('href')
    except:
        link = None

    try:
        title_element = product.find_element(By.CLASS_NAME, "poly-component__title")
        title = title_element.text.strip()
    except:
        title = None

    try:
        price_element = product.find_element(By.CLASS_NAME, "poly-price__current")
        price_text = price_element.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text
        price = Decimal(price_text.replace('.', '').replace(',', '.'))
    except:
        price = None

    try:
        discount_element = product.find_element(By.CLASS_NAME, 'andes-money-amount__discount')
        discount_percentage = Decimal(discount_element.text.replace('% OFF', '').strip())
    except:
        discount_percentage = None

    try:
        previous_price = product.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text.strip()
        previous_price_dec = Decimal(previous_price.replace('.', '').replace(',', '.'))
    except:
        previous_price_dec = None

    try:
        image_element = product.find_element(By.CLASS_NAME, 'poly-component__picture')
        image_url = image_element.get_attribute('data-src') or image_element.get_attribute('src')
        if image_url and 'data:' in image_url:
            image_url = None
    except:
        image_url = None

    try:
        delivery_icon = product.find_element(By.CSS_SELECTOR, 'svg[aria-label="FULL"]')
        tipo_entrega = "Full"
    except:
        tipo_entrega = "Normal"

    try:
        installment_element = product.find_element(By.CLASS_NAME, "poly-price__installments")
        num_installments = installment_element.text.split("x")[0].strip()
        installment_price = installment_element.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text.strip()
        try:
            installment_cents = installment_element.find_element(By.CLASS_NAME, "andes-money-amount__cents").text.strip()
            full_price = f"R$ {installment_price},{installment_cents}"
        except:
            full_price = f"R$ {installment_price}"
        no_interest = "sem juros" in installment_element.text.lower()
        interest_text = "sem juros" if no_interest else "com juros"
        installment_info = f"{num_installments}x de {full_price} {interest_text}"
    except:
        installment_info = None

    # Salva os dados no banco de dados
    produto = Produto(
        imagem=image_url,
        nome=title,
        preco=price,
        parcelamento=installment_info,
        link=link,
        preco_sem_desconto=previous_price_dec,
        percentual_desconto=discount_percentage,
        tipo_entrega=tipo_entrega,
        frete_gratis=tipo_entrega == "Full"
    )
    produto.save()

    print(f"Produto {index} salvo no banco de dados.")

driver.quit()