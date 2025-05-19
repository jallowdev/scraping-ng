from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import csv

# Configuration de Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Exécution en mode sans tête
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

# Remplacez par le chemin vers votre chromedriver
service = Service("./chromedriver/chromedriver.exe")


def scrape_books_with_selenium():
    driver = webdriver.Chrome(service=service, options=chrome_options)
    #driver = webdriver.Firefox(service=service, options=chrome_options)
    base_url = "https://books.toscrape.com/"
    current_page = 1
    books_scraped = 0
    books_data = []

    try:
        while books_scraped < 1000:
            # Construire l'URL de la page actuelle
            if current_page == 1:
                page_url = base_url + "index.html"
            else:
                page_url = base_url + f"catalogue/page-{current_page}.html"

            print(f"Scraping page {current_page} - {page_url}")

            # Charger la page
            driver.get(page_url)
            time.sleep(2)  # Attendre le chargement de la page

            # Trouver tous les livres sur la page
            books = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")

            if not books:
                print("Aucun livre trouvé sur la page. Fin du scraping.")
                break

            for book in books:
                if books_scraped >= 1000:
                    break

                try:
                    # Extraire le titre
                    title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")

                    # Extraire la note
                    rating_class = book.find_element(By.CSS_SELECTOR, "p.star-rating").get_attribute("class").split()[1]
                    rating_map = {
                        'One': 1,
                        'Two': 2,
                        'Three': 3,
                        'Four': 4,
                        'Five': 5
                    }
                    rating = rating_map.get(rating_class, 0)

                    # Extraire le prix
                    price = book.find_element(By.CSS_SELECTOR, "p.price_color").text
                    print(f'# before price : {price}')
                    price = price.replace('Â£', '').strip()
                    price = price.replace('£', '').strip()
                    print(f'# after price : {price}')
                    # Ajouter aux données
                    books_data.append({
                        'title': title,
                        'rating': rating,
                        'price': float(price)
                    })

                    books_scraped += 1
                except NoSuchElementException as e:
                    print(f"Erreur lors de l'extraction d'un livre: {e}")
                    continue

            # Vérifier s'il y a une page suivante
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "li.next a")
                current_page += 1
            except NoSuchElementException:
                print("Pas de page suivante. Fin du scraping.")
                break

            time.sleep(1)  # Politesse

    except Exception as e:
        print(f"Erreur lors du scraping: {e}")
    finally:
        driver.quit()

    return books_data


# Exécution du scraping
books_data = scrape_books_with_selenium()

# Affichage des 5 premiers résultats
print("\nExemple de données scrapées (5 premiers livres):")
for book in books_data[:5]:
    print(book)

# Sauvegarde en CSV
with open('books_selenium.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'rating', 'price']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for book in books_data:
        writer.writerow(book)

print(f"\nScraping terminé. {len(books_data)} livres ont été scrapés et sauvegardés dans books_selenium.csv")