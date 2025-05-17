import requests
from bs4 import BeautifulSoup
import pandas as pd

# Listes pour stocker les données
titres = []
notes = []
prix = []

# Parcourir les 50 pages
for page in range(1, 51):
    url = f'https://books.toscrape.com/catalogue/page-{page}.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Sélectionner tous les articles de livres
    articles = soup.select('article.product_pod')

    for article in articles:
        # Titre
        titre = article.h3.a['title']
        titres.append(titre)

        # Note (extrait de la classe CSS)
        note_classes = article.p['class']
        note = note_classes[1]  # La deuxième classe indique la note
        notes.append(note)

        # Prix (suppression du symbole £)
        prix_text = article.select_one('p.price_color').text
        prix.append(prix_text.replace('£', ''))

# Créer un DataFrame
df = pd.DataFrame({
    'Titre': titres,
    'Note': notes,
    'Prix (£)': prix
})

# Sauvegarder en CSV
df.to_excel('livres_books_to_scrape00.xlsx', index=False)
print("Scraping terminé. Données enregistrées dans 'livres_books_to_scrape.csv'.")
