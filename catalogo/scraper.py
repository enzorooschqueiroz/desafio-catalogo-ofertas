from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = "https://www.mercadolivre.com.br/"
options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(url)
sleep(3)

search_box = driver.find_element(By.ID, "cb1-edit")
search_box.send_keys("Computador Gamer i7 16gb ssd 1tb")
search_box.send_keys(Keys.RETURN)

WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "poly-component__title"))
)

# Capturar os nomes dos produtos e os links
product_elements = driver.find_elements(By.CLASS_NAME, "poly-component__title")

count = 1
# Exibir os resultados
for product in product_elements:
    name = product.text  # Nome do produto
    link = product.get_attribute("href")  # Link do produto
    print(f"Produto: {name}\nLink: {link}\n")
    count += 1
    print(count)
driver.quit()