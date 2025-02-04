from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://lista.mercadolivre.com.br/computador-gamer-i7-16gb-ssd-1tb"
options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(url)
sleep(3)

# Esperar que os elementos dos produtos estejam carregados
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "andes-card"))
)

# Capturar todos os elementos que representam os produtos
product_elements = driver.find_elements(By.CLASS_NAME, "andes-card")

for index, product in enumerate(product_elements, start=1):
    if index > 49:
        break
    
    print("-" * 80)
    
    link_element = driver.find_elements(By.CLASS_NAME, "poly-component__title")
    if link_element:  # Verificar se há elementos na lista
        link = link_element[0].get_attribute('href')  # Acessar o primeiro elemento da lista
        print(f"Link do Produto {index}: {link}")
    else:
        print(f"Erro: Link do Produto {index} não encontrado.")
    
    try:
        # Localizar o título do produto dentro da div do produto usando CLASS_NAME
        title_element = product.find_element(By.CLASS_NAME, "poly-component__title")
        title = title_element.text.strip()
        print(f"Produto {index}: {title}")
    except Exception as e:
        print(f"Erro ao capturar o título do produto {index}: {e}")

    try:
        # Capturar o preço atual
        price_str = product.find_element(By.CLASS_NAME, 'andes-money-amount__fraction').text.replace('.', '').replace(',', '.')
        price = price_str  # Armazenar como string formatada
        print(f"Preço Atual do produto {index}: R$ {price}")
    except Exception as e:
        print(f"Erro no produto {index}: Preço Atual não encontrado.")
        price = None

    discount_percentage = None
    try:
        discount_element = product.find_element(By.CLASS_NAME, 'andes-money-amount__discount')
        discount_percentage = int(discount_element.text.replace('% OFF', '').strip())
        print(f"Desconto: {discount_percentage}%")
    except Exception as e:
        discount_percentage = None

    previous_price = None
    try:
        # Capturar o preço anterior
        previous_price_str = product.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text.strip().replace('.', '')  # Remover ponto
        
        # Verificar se há desconto, caso contrário, não exibe o preço anterior
        if discount_percentage is not None:
            previous_price = previous_price_str
            print(f"Preço anterior do produto {index}: R$ {previous_price}")
        else:
            previous_price = None  # Não mostra o preço anterior se não houver desconto

    except Exception as e:
        print(f"Erro ao capturar o preço anterior do produto {index}: {e}")
        previous_price = None
   
    image_url = None
    try:
        image_element = product.find_element(By.CLASS_NAME, 'poly-component__picture')
        image_url = image_element.get_attribute('data-src') or image_element.get_attribute('src')
        print(f"Imagem do produto: {image_url}")
        if image_url and 'data:' in image_url:
            image_url = None
    except Exception as e:
        print(f"Erro ao capturar a imagem do produto {index}: {e}")


    

    

    print("-" * 80)

driver.quit()
