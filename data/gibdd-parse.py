import requests
from bs4 import BeautifulSoup
import json

url = 'https://xn--80aebkobnwfcnsfk1e0h.xn--p1ai/divisions'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# # Находим все таблицы на странице
divs = soup.find_all('div', class_='b-division-info')
tasks = []
department = []
branches = []

for div in divs:
    dep = div.find('a', class_='b-division-info-title').text
    address = div.find('div', class_='m-t05').text
    department.append((dep, address[7:]))

    d_ = div.find('div', class_='b-division-info-holder')
    # address = d_.find('div', class_='font_14').text
    services = d_.find_all('a', class_='services')
    addresses = d_.find_all('div', class_='font_14')

    for i, service in enumerate(services):
        service = service.text.strip().replace("\n", '')
        branches.append((dep, service, addresses[i].text))
        if service not in tasks:
            tasks.append(service)

service_path = "service.json"
json.dump(tasks, open(service_path, mode='w', encoding='utf-8'), ensure_ascii=False, indent=4)
department_path = "department.json"
json.dump(department, open(department_path, mode='w', encoding='utf-8'), ensure_ascii=False, indent=4)
branches_path = "branches.json"
json.dump(branches, open(branches_path, mode='w', encoding='utf-8'), ensure_ascii=False, indent=4)