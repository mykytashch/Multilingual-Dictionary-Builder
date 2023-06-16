import random
import json
import time
import requests
import sys
from bs4 import BeautifulSoup



USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/94.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 OPR/94.0.4606.81',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Vivaldi/4.4',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0 Waterfox/3.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Whale/3.5.30.17',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 YandexBrowser/21.9.4.194',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Dillo/3.1.4',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Epiphany/40.1.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 SeaMonkey/2.53.10',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Konqueror/21.08',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Falkon/4.1.0'
    # Добавьте свои интересные User-Agent'ы
]

def parse_examples(url, use_proxy=False):
    try:
        headers = {
            'User-Agent': random.choice(USER_AGENTS)
        }

        proxies = None
        if use_proxy:
            proxies = read_proxy_list()

        response = requests.get(url, headers=headers, proxies=proxies)

        soup = BeautifulSoup(response.content, 'html.parser')
        example_divs = soup.find_all('div', {'class': 'example'})

        examples = random.sample(example_divs, k=3)  # Выбираем случайные 3 примера

        result = []
        for div in examples:
            src_text = div.find('div', {'class': 'src'}).text.strip()
            trg_text = div.find('div', {'class': 'trg'}).text.strip()
            example = {'source': src_text, 'target': trg_text}
            result.append(example)

        if not result:
            print("Произошла ошибка: не найдены примеры на странице", url)
        return result

    except requests.exceptions.RequestException as e:
        print("Произошла ошибка при загрузке страницы:", str(e))

def read_proxy_list():
    proxies = []
    with open('proxylist.txt', 'r') as file:
        proxies = [line.strip() for line in file.readlines() if line.strip()]
    return proxies

def main():
    urls = [
        'https://context.reverso.net/translation/english-russian/aforesaid',
        'https://context.reverso.net/translation/english-russian/said',
        'https://context.reverso.net/translation/english-russian/specified',
        'https://context.reverso.net/translation/english-russian/indicated'
    ]

    use_proxy = input("Хотите использовать прокси? (да/нет): ").lower() == "да"

    if use_proxy:
        random.shuffle(USER_AGENTS)  # Перемешиваем список User-Agent'ов, чтобы они соответствовали прокси

    results = {}
    for url in urls:
        word = url.split('/')[-1]
        examples = parse_examples(url, use_proxy)
        results[word] = examples
        time.sleep(1)  # Задержка в 1 секунду

        json_data = json.dumps(results[word], ensure_ascii=False, indent=4)
        print(json_data)
        sys.stdout.flush()  # Очищаем буфер вывода

if __name__ == '__main__':
    main()