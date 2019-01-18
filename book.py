import requests
import csv
import json
class detail:
    def __init__(self, isbn="", title="", author=""):
        self.isbn = isbn
        self.title = title
        self.author = author
    
    def search(self, isbn="", title="", author=""):
        books = open("/Users/utkarsh-mishra/Desktop/learning/project1/books.csv")
        file = csv.DictReader(books)
        book = []
        for row in file:
            if row['isbn'] == self.isbn:
                book.append((row['isbn'], row['title'], row['author'], row["year"]))
            if row['title'] == self.title:
                book.append((row['isbn'], row['title'], row['author'], row["year"]))
            if row['author'] == self.author:
                book.append((row['isbn'], row['title'], row['author'], row["year"]))

        if len(book) == 0:
            return None
        else:
            return list(set(book))

    def get_info(self, isbn):
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "vGOVqMsFwq3CbK0dzrCUA", "isbns": self.isbn})
        print(res.json()["books"][0]["id"])
        book_info = {"isbn": str(res.json()["books"][0]["isbn"]), "review_count": str(res.json()["books"][0]["reviews_count"]), "average_score": str(res.json()["books"][0]["average_rating"])}
        return book_info
    
    
    

