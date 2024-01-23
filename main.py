import requests
from bs4 import BeautifulSoup
import csv

def scrape_content(url, tag, attr, attr_value, pages):
    contents = []

    for page in range(1, pages + 1):
        page_url = f"{url.rstrip('/')}/strona/{page}/"
        response = requests.get(page_url)
        if response.status_code != 200:
            print(f"Problem z połączeniem ze stroną: {page_url}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        if attr and attr_value:
            elements = soup.find_all(tag, {attr: attr_value})
        else:
            elements = soup.find_all(tag)

        for element in elements:
            contents.append(element.get_text(strip=True))

    return contents

def save_to_csv(contents, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for content in contents:
            writer.writerow([content])

url = input("Podaj URL: ")
tag = input("Podaj tag HTML (np. 'h2', 'div'): ")
attr = input("Podaj atrybut HTML (opcjonalnie, np. 'class', ENTER - skip): ")
attr_value = input("Podaj wartość atrybutu (opcjonalnie, ENTER - skip): ")
pages = int(input("Podaj liczbę stron do przeszukania: "))
filename = input("Podaj nazwę pliku CSV: ")

contents = scrape_content(url, tag, attr, attr_value, pages)
save_to_csv(contents, filename)

print(f"Zakończono zapisywanie treści do {filename}")