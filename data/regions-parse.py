import requests
from bs4 import BeautifulSoup
import json

url = 'https://ru.m.wikipedia.org/wiki/%D0%A1%D1%83%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D1%8B_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B9%D1%81%D0%BA%D0%BE%D0%B9_%D0%A4%D0%B5%D0%B4%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D0%B8'  # Замените на нужный URL
response = requests.get(url)


soup = BeautifulSoup(response.text, 'html.parser')

# Находим все таблицы на странице
tables = soup.find_all('table')

t = tables[3]

rows = t.find_all("tr", class_ = lambda x: x != 'dark')
regions = []
rows.pop(0)
rows.pop(-1)
for row in rows:
    cell = row.find('a')
    regions.append(cell.text)

path = "regions.json"
json.dump(regions, open(path, mode='w', encoding='utf-8'), ensure_ascii=False, indent=4)