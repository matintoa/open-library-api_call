import requests
import csv


def get_books(query, limit=50):
    url = "https://openlibrary.org/search.json"
    headers = {
        "User-Agent": "MyBookApp/1.0 (you@example.com)"
    }
    params = {
        "q": query,
        "limit": limit,
        "fields": "key,title,author_name,first_publish_year,cover_i"
    }
    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json().get("docs", [])



books = get_books("python programming", limit=50)
print(f"number of borrowed books {len(books)}")


filtered_books = []


for book in books:
    year = book.get("first_publish_year")

    if year is None:
        continue

    try:
        year = int(year)
    except (ValueError, TypeError):
        continue

   
    if year >= 2000:
        filtered_books.append(book)

filtered_books.sort(
    key=lambda b: b.get("first_publish_year", 0),
    reverse=True
)


print(f" number of after_2000_books {len(filtered_books)}")



with open("books_after_2000.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)

    writer.writerow([
        "title",
        "authors",
        "first_publish_year",
        "key",
        "cover_url"
    ])

    for book in filtered_books:
        cover_i = book.get("cover_i")
        cover_url = (
            f"https://covers.openlibrary.org/b/id/{cover_i}-M.jpg"
            if cover_i else ""
        )

        writer.writerow([
            book.get("title", ""),
            ", ".join(book.get("author_name", [])),
            book.get("first_publish_year", ""),
            book.get("key", ""),
            cover_url
        ])

print(" file (books_after_2000.csv) saved")