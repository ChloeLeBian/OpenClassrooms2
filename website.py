import requests
from bs4 import BeautifulSoup 
from function import getAllCategory
from function import getAllBookLinkByCategory
from function import getBookData
import csv
import time

print('begin scraping') 

main_url = 'http://books.toscrape.com/index.html'
categories_url=getAllCategory(main_url)
#on va chercher les catégories grâce à la fonction catégorie avec l'url de la page d'accueil

for category_url in categories_url:
    #on crée une boucle pour chaque url de la liste categories_url

    category=category_url.replace('http://books.toscrape.com/catalogue/category/books/','')
    category=category.replace('/index.html','')
    #on récupère le nom de la catégorie

    books_url=getAllBookLinkByCategory(category_url)
    #on récupère les urls des livres pour chaque catégorie

    with open(f'data/{category}.csv', 'w', newline='') as csvfile:
        #on crée un document csv pour chaque catégorie dans lequel on va écrire
        fieldnames = ['book_url','universal_product_code','title','price_including_tax','price_excluding_tax','number_available','product_description','category','review_rating','image_url']
        #on renseigne le nom des champs
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()


        for book_url in books_url:
            #on crée une boucle pour pour chaque url de livre dans la liste d'url récupéré par catégorie
            bookData=getBookData(book_url)
            #on récupère les données dont on a besoin pour chaque livre
            writer.writerow(bookData)
            #on assigne ces données aux champs renseignés dans le fichier csv
            
            image_url = bookData['image_url']
            title = bookData['title']
            #on récupère également dans notre dictionnaire l'url du livre et le son titre

            with open(f'images/{title}.jpg', 'wb') as f:
                #on crée un fichier jpg que l'on met dans notre dossier 'images' et dont le nom est le titre du livre
                image = requests.get(image_url)
                #on va chercher l'image et on la place dans le dossier
                f.write(image.content)

    time.sleep(3)
    #on arrête le programme 3 secondes entre chaque catégorie pour ne pas que le site nous bloque à cause du nombre de requêtes
            
print('end scraping')
    