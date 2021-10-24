import shutil
import os

import requests
from bs4 import BeautifulSoup
import csv342 as csv


def download(url, pathname):
    if not os.path.isdir(pathname): os.mkdir(pathname)
    filename = pathname + "/" + url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=1048576):
                f.write(chunk)
    return filename


def BookData(url):
    url = "http://books.toscrape.com/catalogue/" + url
    page = requests.get(url)
    page.encoding = "utf-8"
    soup = BeautifulSoup(page.content, 'html.parser')
    # Extraire les données de la page
    product_page_url = url
    table = soup.find("table", class_="table table-striped").contents
    upc = table[1].contents[2].string
    price_excluding_tax = table[5].contents[2].string
    price_including_tax = table[7].contents[2].string.split('£')[-1].replace(".", ",")
    stock = table[11].contents[3].string
    number_available = stock[stock.index("(")+1:-11]
    review_rating = table[13].contents[3].string
    title = soup.title.string[0:-28].strip()
    print(title)
    try:
        product_description = soup.find(id="product_description").next_sibling.next_sibling.string
    except AttributeError:
        product_description =""
    category = soup.find_all("a", href=True)[3].string
    url_image = soup.find("img")['src']
    image_url = "http://books.toscrape.com/" + url_image[6:len(url_image)]
    # Générer la liste des variables dans Book_Data
    Book_Data = [product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available,
                 product_description, category, review_rating, image_url]
    return Book_Data


def BookEntete(nom):
    en_tete = ["product_page_url", "universal_product_code (upc)", "title", "price_including_tax",
               "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
    # ouverture du fichier CSV avec le paramètre encoding='utf-8-sig' pour générer le byte-order-mark (bom) reconnu par Excel
    with open(nom, 'w', newline='', encoding='utf-8-sig') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=';')
        writer.writerow(en_tete)
    return


def BookCSV(nom, ligne):
    with open(nom, 'a', newline='', encoding='utf-8-sig') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=';')
        writer.writerow(ligne)
    return


def BookPageCategory(url, fichier, url_origine, pathname):
    extend_url = "http://books.toscrape.com/catalogue/category/books/" + url
    page = requests.get(extend_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    liste_url = soup.find_all("h3")
    # Pour tous les livres de la page, recupérer les données, les copier dans le fichier csv et copier l'image
    for index in range(len(liste_url)):
        book_url = liste_url[index].contents[0]['href'][9:-11]
        newline = BookData(book_url)
        BookCSV(fichier, newline)
        filename = download(newline[9], pathname)
        # limite du nom de fichier des images de couverture à 50 caractères
        newFilename = book_url[0: len(book_url)-len(book_url.split("_")[-1])-1]
        while len(newFilename) > 50:
            newFilename = newFilename[0: len(newFilename)-len(newFilename.split("-")[-1])-1]
        os.rename(filename, pathname + "/" + newFilename + "_" + book_url.split("_")[-1] + ".jpg")
    nombrelivre = int(soup.find(class_="form-horizontal").contents[3].string)
    showlivre = nombrelivre
    if nombrelivre > 20:
        showlivre = int(soup.find(class_="form-horizontal").contents[7].string)
    next = False
    next_url = ""
    if showlivre < nombrelivre:
        next_url = url_origine + "/" + soup.find(class_="next").contents[0]['href']
        next = True
    return next, next_url, url_origine


def BookCategory(url, pathname):
    pathname = pathname + "/" + url
    if not os.path.isdir(pathname): os.mkdir(pathname)
    filename = pathname + "/Books_" + url + ".csv"
    BookEntete(filename)
    suivant = BookPageCategory(url, filename, url, pathname)
    while suivant[0]:
        suivant = BookPageCategory(suivant[1], filename, url, pathname)


# Programme principal
# Génération des fichiers csv et téléchargement des images dans un répertoire par catégorie

page = requests.get("http://books.toscrape.com")
soup = BeautifulSoup(page.content, 'html.parser')
repertoire = "Books"
if os.path.isdir(repertoire): shutil.rmtree(repertoire)
os.mkdir(repertoire)

category = soup.find(class_="nav nav-list").contents[1].contents[3]
impair = False
for item in category:
    if impair:
        urlcategory = item.contents[1]['href'][25:-11]
        print('\033[92m', urlcategory, '\033[0m')
        BookCategory(urlcategory, repertoire)
    impair = not(impair)
