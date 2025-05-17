import logging
import time

import requests
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)


def scrape_books_to_1000():
    base_url = "https://books.toscrape.com/"
    current_page = 1
    books_scraped = 0
    books_data = []
    last_book = 2000

    while books_scraped < last_book:
        # Construire l'URL de la page actuelle
        if current_page == 1:
            page_url = base_url + "index.html"
        else:
            page_url = base_url + f"catalogue/page-{current_page}.html"

        print(f"Scraping page {current_page}...")

        try:
            # Récupérer le contenu de la page
            response = requests.get(page_url)
            response.raise_for_status()

            # Parser le HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Trouver tous les livres sur la page
            books = soup.find_all('article', class_='product_pod')

            if not books:
                print("Aucun livre trouvé sur la page. Fin du scraping.")
                break

            for book in books:
                if books_scraped >= last_book:
                    break

                # Extraire le titre
                title = book.h3.a['title']

                # Extraire la note (convertie en nombre)
                rating_class = book.p['class'][1]
                rating_map = {
                    'One': 1,
                    'Two': 2,
                    'Three': 3,
                    'Four': 4,
                    'Five': 5
                }
                rating = rating_map.get(rating_class, 0)

                # Extraire le prix
                price = book.find('p', class_='price_color').text
                price = price.replace('Â£', '')  # Nettoyer le symbole de livre

                # Ajouter les données à la liste
                books_data.append({
                    'title': title,
                    'rating': rating,
                    'price': float(price)
                })

                books_scraped += 1

            # Vérifier s'il y a une page suivante
            next_button = soup.find('li', class_='next')
            if not next_button and books_scraped < last_book:
                print("Pas de page suivante. Fin du scraping.")
                break

            current_page += 1
            time.sleep(1)  # Respecter le politeness delay

        except Exception as e:
            print(f"Erreur lors du scraping de la page {current_page}: {e}")
            break

    return books_data


# Exécuter la fonction de scraping
books_data = scrape_books_to_1000()

# Afficher les 5 premiers livres à titre d'exemple
print("\nExemple de données scrapées (5 premiers livres):")
for book in books_data[:5]:
    print(book)

# Sauvegarder dans un fichier CSV
import csv

with open('books_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'rating', 'price']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for book in books_data:
        writer.writerow(book)

print(f"\nScraping terminé. {len(books_data)} livres ont été scrapés et sauvegardés dans books_data.csv")
