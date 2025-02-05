from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from decimal import Decimal

url = "https://lista.mercadolivre.com.br/computador-gamer-i7-16gb-ssd-1tb"
options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(url)
sleep(3)

WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "andes-card"))
)

product_elements = driver.find_elements(By.CLASS_NAME, "andes-card")

sleep(2)
for index, product in enumerate(product_elements, start=1):
    if index == 1:
        continue

    if index > 49:
        break
    
    print("-" * 80)
    
    # Link do Produto
    try:
        link_element = product.find_element(By.CLASS_NAME, "poly-component__title") 
        link = link_element.get_attribute('href')
        print(f"Link do Produto {index}: {link}")
    except:
        print(f"Erro: Link do Produto {index} não encontrado.")

    # Nome do Produto
    try:
        title_element = product.find_element(By.CLASS_NAME, "poly-component__title")
        title = title_element.text.strip()
        print(f"Produto {index}: {title}")
    except Exception as e:
        print(f"Erro ao capturar o título do produto {index}: {e}")

    # Preço Atual do Produto
    try:
        price_element = product.find_element(By.CLASS_NAME, "poly-price__current")
        price_text = price_element.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text
        price = Decimal(price_text.replace('.', '').replace(',', '.'))
        print(f"Preço Atual do produto {index}: R$ {price}")
    except Exception as e:
        print(f"Erro ao capturar o preço atual do produto {index}: {e}")

    # Porcentagem de Desconto
    discount_percentage = None
    try:
        discount_element = product.find_element(By.CLASS_NAME, 'andes-money-amount__discount')
        discount_percentage = Decimal(discount_element.text.replace('% OFF', '').strip())
        print(f"Desconto: {discount_percentage}%")
    except Exception as e:
        discount_percentage = None

    # Preço Antes do Desconto
    try:
        previous_price = product.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text.strip()
        previous_price_dec = Decimal(previous_price.replace('.', '').replace(',', '.'))
        if discount_percentage is not None:
            print(f"Preço Anterior do produto {index}: R$ {previous_price_dec}")
        else: 
            previous_price_dec = None
    except:
        previous_price_dec = None
        print(f"Preço Anterior do produto {index} não encontrado.")

    # URL da Imagem
    image_url = None
    try:
        image_element = product.find_element(By.CLASS_NAME, 'poly-component__picture')
        image_url = image_element.get_attribute('data-src') or image_element.get_attribute('src')
        print(f"Imagem do produto: {image_url}")
        if image_url and 'data:' in image_url:
            image_url = None
    except Exception as e:
        print(f"Erro ao capturar a imagem do produto {index}: {e}")

    # Tipo de Entrega
    try:
        delivery_icon = product.find_element(By.CSS_SELECTOR, 'svg[aria-label="FULL"]')
        tipo_entrega = "Full"
        print(f"Tipo de Entrega: {tipo_entrega}")
    except Exception as e:
        tipo_entrega = "Normal"
        print(f"Tipo de Entrega: {tipo_entrega}")

    # Opção de Parcelamento:
    try:
        installment_element = product.find_element(By.CLASS_NAME, "poly-price__installments")

        # Capturar a quantidade de parcelas
        num_installments = installment_element.text.split("x")[0].strip()

        # Capturar o valor da parcela (parte inteira)
        installment_price = installment_element.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text.strip()

        # Tentar capturar os centavos (se existir)
        try:
            installment_cents = installment_element.find_element(By.CLASS_NAME, "andes-money-amount__cents").text.strip()
            full_price = f"R$ {installment_price},{installment_cents}"
        except:
            full_price = f"R$ {installment_price}"  # Se não houver centavos, mantém só a parte inteira

        # Verificar se há "sem juros"
        no_interest = "sem juros" in installment_element.text.lower()
        interest_text = "sem juros" if no_interest else "com juros"

        # Criar a string formatada
        installment_info = f"{num_installments}x de {full_price} {interest_text}"

        print(f"Parcelamento: {installment_info}")

    except Exception as e:
        print(f"Erro ao capturar o parcelamento do produto {index}: {e}")



    print("-" * 80)

driver.quit()
