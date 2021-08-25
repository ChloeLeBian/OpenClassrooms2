import requests
from bs4 import BeautifulSoup 

def getAllCategory(url):
    #on récupère les url des catégories sur la page d'accueil
    response1 = requests.get(url)
    soup = BeautifulSoup(response1.text, 'html.parser')

    categories = soup.find('ul',{'class','nav-list'})
    lis= categories.findAll('li')
    
    categories_url=[]
    #on crée une liste vide pour y mettre les liens url de nos catégories
    
    for li in lis:
        a=li.find('a')
        category_url=a['href']
        #pour chaque lien, l'url de la catégorie est après la mention 'href'
        
        if category_url != 'catalogue/category/books_1/index.html':
            #si l'url de la catégorie n'est pas celui de la page d'accueil 
            category_url='http://books.toscrape.com/' + category_url

            categories_url.append(category_url)
            #on ajoute l'url final à notre liste
    
    return categories_url



def getAllBookLinkByCategory(category_url):
    #on récupère les liens url des livres pour chaque catégorie
    
    books_url=[]
    #on crée une liste vide pour y mettre les liens url de nos livres

    response2 = requests.get(category_url)
    soup = BeautifulSoup(response2.text, 'html.parser')
    numberOfBooks = soup.find('form',{'class': 'form-horizontal'})
    numberOfBooks = numberOfBooks.find('strong')
    numberOfBooks = numberOfBooks.text
    numberOfBooks = int(numberOfBooks)
    #on récupère pour chaque catégorie le nombre de livres car selon le nombre de livres, les url des pages seront légérement différents

    if numberOfBooks > 20:
        #s'il y a plus de 20 livres dans une catégorie, alors il y a plusieurs pages à scrapper. Nous allons crée une boucle par page, et composer son url.

        for i in range(1,15):
            category_url=category_url.replace('index.html','')
            response = requests.get(category_url + 'page-' + str(i) + '.html')
            soup = BeautifulSoup(response.text, 'html.parser')

            lis = soup.findAll('li', {'class', 'col-xs-6'})

            for li in lis:
                a = li.find('a')
                book_url=a['href']
                book_url= book_url.replace('../../..','http://books.toscrape.com/catalogue')

                books_url.append(book_url)
                #nous ajoutons les url trouvés à notre liste

        return books_url

    else:
        #s'il y a moins de 20 livres dans une catégories, alors la page unique à scrapper et celle que nous avions trouvé grâce à la fonction précédente.
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        lis = soup.findAll('li', {'class', 'col-xs-6'})

        for li in lis:
            a = li.find('a')
            book_url=a['href']
            book_url= book_url.replace('../../..','http://books.toscrape.com/catalogue')

            books_url.append(book_url)
            #nous ajoutons les url trouvés à notre liste

        return books_url  


def getBookData(book_url):
    #nous cherhons les données sur chaque livre

    bookData={}
    #nous créons un dictionnaire vide pour y classer nos données

    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    bookData['book_url'] = book_url
    #nous ajoutons l'url du livre à notre dictionnaire sous la clé 'book_url'

    infos = soup.findAll('td')

    universal_product_code = infos[0].text
    bookData['universal_product_code'] = universal_product_code
    #nous ajoutons le code du livre à notre dictionnaire sous la clé 'universal_product_code'

    title = soup.find('h1')
    title = title.text
    bookData['title'] = title
    #nous ajoutons le titre du livre à notre dictionnaire sous la clé 'title'

    price_including_tax = infos[3].text
    price_including_tax = price_including_tax.replace('Â£','')
    bookData['price_including_tax'] = price_including_tax
    #nous ajoutons le prix TTC livre à notre dictionnaire sous la clé 'price_including_tax'
    

    price_excluding_tax = infos[2].text
    price_excluding_tax = price_excluding_tax.replace('Â£','')
    bookData['price_excluding_tax'] = price_excluding_tax
    #nous ajoutons le prix HT livre à notre dictionnaire sous la clé 'price_excluding_tax'

    number_available = infos[5].text
    number_available = number_available.replace('In stock (', '')
    number_available = number_available.replace('available)','')
    number_available = number_available.lstrip()
    bookData['number_available'] = number_available
    #nous ajoutons le nombre de livres disponibles à notre dictionnaire sous la clé 'number available'

    product_description = soup.find('meta',{'name': 'description'})
    product_description = product_description['content']
    product_description = product_description.strip()
    bookData['product_description'] = product_description
    #nous ajoutons la description du livre à notre dictionnaire sous la clé 'product_description'

    ul = soup.find('ul', {'class': 'breadcrumb'})
    lis = ul.findAll('li')
    category = lis[2].text
    bookData['category'] = category.strip()
    #nous ajoutons le catégorie du livre à notre dictionnaire sous la clé 'category'

    elements = soup.find('p', {'class': 'star-rating'})
    elements=elements['class']
    review_rating = elements[1]

    if review_rating == 'One':
        review_rating=1
    elif review_rating == 'Two':
        review_rating=2
    elif review_rating == 'Three':
        review_rating=3
    elif review_rating == 'Four':
        review_rating=4
    elif review_rating == 'Five':
        review_rating=5
    else:
        review_rating='no review'
    
    bookData['review_rating'] = review_rating
    #nous ajoutons le rating du livre à notre dictionnaire sous la clé 'review_rating'

    image = soup.find('img')
    image_url = image['src']
    image_url = image_url.replace('../..', 'http://books.toscrape.com/')
    bookData['image_url'] = image_url
    #nous ajoutons l'url de l'image du livre à notre dictionnaire sous la clé 'image_url'

    return bookData








