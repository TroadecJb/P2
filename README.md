# P2 - Surveillance des prix

Extracts data off [BooksToScrape](https://books.toscrape.com/).  
Writes a CSV file for each category with several informations about each book:
 - title
 - description
 - category
 - upc
 - price (incl. tax)
 - price (excl. tax)
 - availabilty
 - rating
 - product page url
 - cover's url

# Environment

To use this script in an vitrual environment, follow these steps.

Python>=3.10.7

```
$ cd /path/to/project
$ python -m -venv <environment name>
```

activation windows\
```$ ~env\Scripts\activate.bat```\
activation macos\
```$ ~source env/bin/activate```\

packages installation\
```(env)$ python -m pip install -r requirements.txt```

*for further details, [click here](https://docs.python.org/fr/3/library/venv.html#venv-def)*

# Requirements

Beautifulsoup4==4.11.1\
requests==2.28.1

# Information

This script will create a main folder **BooksToScrape** in the current work directory.  
Two subfolders **csv** and **books_cover**.  
In the **csv** sublfoder, a csv file for each category will be created.
Each row will represent a book.  
In the **books_cover** subfolder, a folder will be created for each category.  
In each of those folders, the image of each book's cover will be saved under the book's title.