import logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

log = logging.getLogger(__name__)

try:
    # Configuration des options du navigateur
    options = Options()
    # options.add_argument("--headless")  # Mode sans interface graphique
    options.add_argument("--disable-gpu")  # Désactive l'accélération GPU
    options.add_argument("--no-sandbox")  # Nécessaire pour certains environnements Linux

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://visa.vfsglobal.com/sen/fr/prt/login")

    time.sleep(30)

    cookies = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
    if cookies:
        print(f'### COOKIES {cookies.text}')
        cookies .click()

    isCheck = driver.find_element(By.XPATH, '//*[@id="wBIvQ7"]/div/label/input')
    #isCheck = driver.find_element(By.XPATH, '//*[@id="wBIvQ7"]/div/label/input')
    if isCheck:
        print(f'### isCheck {isCheck.text}')
        isCheck.click()

    time.sleep(30)



except Exception as ex:
    log.info(f'ERROR DE CONNEXION : {ex}')
