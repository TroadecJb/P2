# P2 - Surveillance des prix
___
Extract data off [BooksToScrape](https://books.toscrape.com/).
Write a CSV file for each category with several informations about each book:
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
___
Python>=3.10.7
Beautifulsoup4==4.11.1
requests==2.28.1

# Information
___
This script will create a main folder **BooksToScrape** in the current work directory.
Two subfolders **csv** and **books_cover**.
In the **csv** sublfoder, a csv file for each category will be created.
Each row will represent a book.
In the **books_cover** subfolder, a folder will be created for each catageroy.
In each of those folders the image of each book's cover will be saved and the book's title.