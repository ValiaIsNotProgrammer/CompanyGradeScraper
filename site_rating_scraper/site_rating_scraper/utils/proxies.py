import requests
import os

PROXY_LIST_FILE = os.path.join(os.getcwd(), 'proxies.txt')


def fetch_proxies(count):

    if not os.path.exists(PROXY_LIST_FILE):
        url = 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt'
        response = requests.get(url)
        if response.status_code == 200:
            proxy_list = response.text.split('\n')[::-count]
            with open(PROXY_LIST_FILE, 'w') as f:
                f.write('\n'.join(proxy_list))

            print("Прокси загружены и сохранены в файл 'proxies.txt'")
        else:
            print(f"Ошибка при загрузке прокси: {response.status_code}")
    else:
        print(f"Прокси взяты из файла 'proxies.txt'")

    return PROXY_LIST_FILE

