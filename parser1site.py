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

def load_word_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        word_list = file.read().splitlines()
    return word_list

def parse_examples(url):
    try:
        headers = {
            'User-Agent': random.choice(USER_AGENTS)
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        examples = []
        example_divs = soup.find_all('div', {'class': 'example'})

        for div in example_divs:
            src_text = div.find('div', {'class': 'src'}).text.strip()
            trg_text = div.find('div', {'class': 'trg'}).text.strip()
            example = {'source': src_text, 'target': trg_text}
            examples.append(example)

        return examples[:3]

    except requests.exceptions.RequestException:
        return []

def main():
    start_word = int(input("С какого слова начинаем? (от 1): "))
    end_word = int(input("На каком слове заканчиваем? (до 236736): "))

    word_list = load_word_list('word_list.txt')
    selected_words = word_list[start_word-1:end_word]

    urls = [
        f"https://context.reverso.net/translation/english-russian/{word}" for word in selected_words
    ]

    results = {}
    for url in urls:
        examples = parse_examples(url)
        word = url.split('/')[-1]
        results[word] = examples
        time.sleep(1)  # Задержка в 1 секунду

        json_data = json.dumps({word: examples}, ensure_ascii=False, indent=4)
        print(json_data)

if __name__ == '__main__':
    main()