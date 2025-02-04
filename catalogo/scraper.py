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
    
    try:
        # Localizar o título do produto dentro da div do produto usando CLASS_NAME
        title_element = product.find_element(By.CLASS_NAME, "poly-component__title")
        title = title_element.text.strip()
        print(f"Produto {index}: {title}")
    except Exception as e:
        print(f"Erro ao capturar o título do produto {index}: {e}")

driver.quit()
