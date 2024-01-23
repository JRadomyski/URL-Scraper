import os
import requests
from bs4 import BeautifulSoup
import csv

def scrape_content(base_url, tag, attr, attr_value, pages):
    contents = []

    for page in range(1, pages + 1):
        page_url = f"{base_url.rstrip('/').rsplit('/', 1)[0]}/{page}/"
        print(f"Przetwarzanie strony: {page_url}")

        try:
            response = requests.get(page_url, timeout=5)
            if response.status_code != 200:
                print(f"Nie znaleziono strony: {page_url}")
                continue

            soup = BeautifulSoup(response.content, 'html.parser')
            if attr and attr_value:
                elements = soup.find_all(tag, {attr: attr_value})
            else:
                elements = soup.find_all(tag)

            for element in elements:
                contents.append(element.get_text(strip=True))

            print("Pierwsze elementy na stronie:", contents[-5:])

        except requests.RequestException as e:
            print(f"Błąd podczas łączenia ze stroną: {page_url} - {e}")
            continue

    return contents

def save_to_csv(contents, filename):
    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    path = os.path.join('outputs', filename)
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for content in contents:
            writer.writerow([content])


base_url = input("Podaj URL pierwszej strony (np. 'https://tezeusz.pl/blog/motywy/strona/1/'): ")
tag = input("Podaj tag HTML (np. 'h2', 'div'): ")
attr = input("Podaj atrybut HTML (opcjonalnie, np. 'class', ENTER - skip): ")
attr_value = input("Podaj wartość atrybutu (opcjonalnie, ENTER - skip): ")
pages = int(input("Podaj liczbę stron do przeszukania: "))
filename = input("Podaj nazwę pliku CSV: ")

contents = scrape_content(base_url, tag, attr, attr_value, pages)
save_to_csv(contents, filename)

print(f"Zakończono zapisywanie treści do folderu 'outputs' w pliku {filename}")
