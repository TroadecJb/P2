import requests
from bs4 import BeautifulSoup
import re
import csv
from pathlib import Path
import os

#########
def parse(url):
    '''
    Parse a url (.content, 'hmtl.parser'), returns the soup
    '''
    response = requests.get(url)
    page = response.content
    soup = BeautifulSoup(page, 'html.parser')
    return soup

def has_next_page(soup):
    '''
    Returns True if the provided page has a next page.
    '''
    if soup.find('li', {'class': 'next'}):
        return True
    else:
        return False

def cleanName(inputName):
    '''
    Removes characters that might cause an issue in filename.
    Works on Windows, should works in MacOs and Linux.
    '''
    unwantedChar = '"%:/,.\\[]<>*?'
    return ''.join([c for c in inputName if c not in unwantedChar])

def get_categories(url):
    '''
    Get a dictionary of every category and their urls.
    '''
    dict_categories = {}
    
    soup = parse(url)
    
    categories = soup.find('ul', {'class', 'nav nav-list'}).find_all('a')
    for category in categories[1:]:
        x = category.get_text(strip=True)
        dict_categories[x] = [url + category.get('href')]
    print('list of categories:\n\tdone')
    return dict_categories

def get_pages_of_category(dict_categories):
    '''
    Update the variable in arg with all the pages for each category.
    '''
    for category, pages in dict_categories.items():
        print(f"\n{category}_")
        url_base = pages[0]
        for page in pages:
            soup = parse(page)

            if has_next_page(soup):
                next_url = soup.find('ul', {'class': 'pager'}).find('li', {'class': 'next'}).find('a').get('href')
                next_page = url_base[:-10] + next_url
                pages.append(next_page)
        print(f"\tfound: {len(pages)} page(s).")

def get_category_books_link(dict_categories_pages):
    '''
    Get the link of every books of a category through multiple pages.
    Returns a dictionary (key=category, value=list of books url).
    '''  
    print(f"\n\t- - - Start : getting every book's url by category - - - ")
    category_books_url = {}

    for category, urls in dict_categories_pages.items():
        print(f"\n\t- {category} -")
        
        list_url = []
        for idx, url in enumerate(urls):
            soup = parse(url)
            list_books = soup.find_all('article', {'class': 'product_pod'})

            for book in list_books:
                link = book.find('a').get('href')
                url_base = 'https://books.toscrape.com/catalogue'
                list_url.append(url_base + link[8:])
            
            category_books_url[category] = list_url
            print(f"\tpage {idx + 1} over {len(urls)}")
        print(f"\tbooks found : {len(list_url)}")
        print(f" \t-end-")
    print(f"\n\t- - - End : getting every book's url by category - - - ")
    return category_books_url

def get_books_data(dict_categories_books_url):
    """
    Extracts data about a book page from a given dictionary (key=category, value=list of books url).
    Writes a csv for each category into subfolder "csv".
    Saves covers of every books into categories' subfolder of "booksCover".
    """

    # Create folder 'BooksToScrape' and subfolders into the current working directory
    folder = Path.cwd() / ('BooksToScrape')
    csvFolder = os.path.abspath(folder / Path('csv'))
    booksCover = os.path.abspath(folder / Path('books_cover'))
    os.makedirs(csvFolder)
    os.makedirs(booksCover)

    for category, books_url in dict_categories_books_url.items():
        data_by_category = {}

        # Create subfolder for each categorie covers.
        coverCategory = os.path.abspath(booksCover / Path(f"{category}_cover"))
        os.makedirs(coverCategory)

        # Create csv for the category
        header = ["title", "category", "description", "review_rating", "image_url", "upc", "price_incl_tax", "price_excl_tax", "availability"]
        print(f"writing {category} csv.")
        for idx, link in enumerate(books_url):
            data_by_category[f"{idx + 1}"] = {}
            soup = parse(link)
            
            # titre
            titre = soup.find('h1').text # var use later for cover.jpg's name
            data_by_category[f"{idx + 1}"]['title'] = titre

            # categorie
            data_by_category[f"{idx + 1}"]['category'] = f"{category}"

            # description
            if soup.find('article', {'class': 'product_page'}).find('p', {'class': ''}) == True:
                data_by_category[f"{idx + 1}"]['description'] = soup.find('article', {'class': 'product_page'}).find('p', {'class': ''}).text
            else:
                data_by_category[f"{idx + 1}"]['description'] = 'no description'

            # rating
            rating = soup.find('p', class_=re.compile('star-rating'))
            data_by_category[f"{idx + 1}"]['review_rating'] = rating['class'][1]

            # Image URL
            image = soup.find('img').get('src')
            imageLink = 'https://books.toscrape.com' + image[5:] # var use below to download the cover
            data_by_category[f"{idx + 1}"]['image_url'] = imageLink
            
            # Download image to folder 'booksCover'
            cover = open(os.path.abspath(coverCategory)+'/'+f"{cleanName(titre)}.jpg", 'wb')
            cover.write(requests.get(imageLink).content)
            cover.close()

            # Tableau (upc, prix, stock, avis)
            table = soup.find('table', {'class': 'table table-striped'})
            for row in table.find_all('tr'):
                cat = row.find('th').text
                value = row.find('td').text
                if cat == 'UPC':
                    data_by_category[f"{idx + 1}"]['upc'] = value
                elif cat == 'Price (excl. tax)':
                    data_by_category[f"{idx + 1}"]['price_excl_tax'] = value
                elif cat == 'Price (incl. tax)':
                    data_by_category[f"{idx + 1}"]['price_incl_tax'] = value
                elif cat == 'Availability':
                    data_by_category[f"{idx + 1}"]['availability'] = value
        
        with open(os.path.abspath(csvFolder)+'/'+f"{category}.csv", 'w', newline='', encoding='utf-8') as category_csv:
            writer = csv.writer(category_csv)
            writer.writerow(header)
            for book, datas in data_by_category.items():
                writer.writerow(datas.values())
                print(f"\t{datas['title']}")
                
        print(f"{category}.csv finished\n")
    print("csv and books' cover saved under 'BooksToScrape' folder")

def main():
    url = 'https://books.toscrape.com/'
    categories = get_categories(url)
    get_pages_of_category(categories)
    booksUrl = get_category_books_link(categories)
    get_books_data(booksUrl) 
#########

if __name__=="__main__":
    main()