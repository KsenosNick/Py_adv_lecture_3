import bs4
import requests
import re

KEYWORDS = {'дизайн', 'Фото', 'web', 'python', 'Автоматизация'}


def main(words_set):
    response = requests.get('https://habr.com/ru/all/')
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, features='html.parser')
    articles = soup.find_all('article')

    words_list = list(words_set)
    words_list_lower = []
    for word in words_list:
        words_list_lower.append(word.lower())
    words_set = set(words_list_lower)

    for article in articles:
        if article.find("h2") is not None:
            header = article.find("h2").text
            header_clear = re.sub("[^a-zA-Zа-яА-Я0-9]", " ", header)
            header_set = set(header_clear.lower().split(' '))
        if article.find(class_='tm-article-body tm-article-snippet__lead') is not None:
            article_text = article.find(class_='tm-article-body tm-article-snippet__lead').text.strip()
            article_text_clear = re.sub("[^a-zA-Zа-яА-Я0-9]", " ", article_text)
            article_set = set(article_text_clear.lower().split(' '))
        if article.find_all(class_='tm-article-snippet__hubs-item') is not None:
            hubs = article.find_all(class_='tm-article-snippet__hubs-item')
            hubs_set = set(hub.find('span').text.lower().strip() for hub in hubs)
        if article.find(class_='tm-article-snippet__datetime-published') is not None:
            date_time = article.find(class_='tm-article-snippet__datetime-published').text
        if article.find(class_='tm-article-snippet__title-link') is not None:
            href = article.find(class_='tm-article-snippet__title-link').attrs['href']
            link = 'https://habr.com' + href
        response_full = requests.get(link)
        response_full.raise_for_status()
        soup_full = bs4.BeautifulSoup(response_full.text, features='html.parser')
        article_full = soup_full.find('article')
        if article_full.find(class_='tm-article-body') is not None:
            article_full_text = article_full.find(class_='tm-article-body').text.strip()
            article_full_text_clear = re.sub("[^a-zA-Zа-яА-Я0-9]", " ", article_full_text)
            article_full_set = set(article_full_text_clear.lower().split(' '))

        article_all = header_set | article_set | hubs_set | article_full_set

        if words_set & article_all:
            print(f'{date_time} - {header} - {link}')

if __name__ == '__main__':
    main(KEYWORDS)