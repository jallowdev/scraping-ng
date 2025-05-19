from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configuration des options du navigateur
options = Options()
options.add_argument("--start-maximized")  # Ouvre le navigateur en plein écran

# Chemin vers le ChromeDriver
# chrome_driver_path = '/chemin/vers/chromedriver'  # Remplacez par le chemin réel

# Initialisation du service et du navigateur
service = Service("./chromedriver/chromedriver.exe")
# Configurer Selenium avec Chrome
driver = webdriver.Chrome(service=service, options=options)
#driver = webdriver.Chrome(ChromeDriverManager().install())

# Maximiser la fenêtre
driver.maximize_window()

# 1. Accéder à la page de login
driver.get("https://boredevances.diotali.com/login")

# Attendre que la page soit chargée
wait = WebDriverWait(driver, 10)

try:
    # 2. Trouver les champs de connexion (inspecter la page pour vérifier les sélecteurs)
    email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))  # ou By.ID, By.CSS_SELECTOR
    password_input = driver.find_element(By.NAME, "password")  # ajuster selon la page
    login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Se connecter')]")  # ou autre sélecteur

    # 3. Remplir les identifiants (à remplacer par vos données)
    email_input.send_keys("ibrahima.diallo@diotali.com")
    password_input.send_keys("Dia@4321")

    # 4. Cliquer sur le bouton de connexion
    login_button.click()

    # 5. Attendre la redirection ou un élément de la page d'accueil
    wait.until(EC.url_contains("/dashboard"))  # ou vérifier un élément spécifique
    print("✅ Connexion réussie !")

except Exception as e:
    print(f"❌ Erreur lors de la connexion : {e}")
    # Prendre une capture d'écran en cas d'échec
    driver.save_screenshot("erreur_connexion.png")

# Attendre 5 secondes pour observer le résultat
time.sleep(5)

# Fermer le navigateur
driver.quit()