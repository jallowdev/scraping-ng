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
    driver.get("https://boredevances.diotali.com/login")
    time.sleep(2)
    driver.find_element(By.XPATH,
                        "/html/body/app-root/app-login/div/nz-row[2]/nz-col[2]/nz-row/nz-card/div/form/nz-form-item[1]/nz-form-control/div/div/nz-input-group/input").send_keys(
        "ibrahima.diallo@diotali.com")
    driver.find_element(By.XPATH,
                        "/html/body/app-root/app-login/div/nz-row[2]/nz-col[2]/nz-row/nz-card/div/form/nz-form-item[2]/nz-form-control/div/div/nz-input-group/input").send_keys(
        "*******")
    driver.find_element(By.XPATH,
                        "/html/body/app-root/app-login/div/nz-row[2]/nz-col[2]/nz-row/nz-card/div/form/button").click()
    log.info(f'SUCCESS CONNEXION')

    elements = driver.find_elements(By.XPATH, "/html/body/app-root/app-welcome/nz-layout/nz-layout/nz-content/div")
    for elem in elements:
        print(f"{elem.tag_name}: {elem.text.strip()}")

    time.sleep(10)
    driver.quit()

except Exception as ex:
    log.info(f'ERROR DE CONNEXION : {ex}')
