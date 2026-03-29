import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from datetime import datetime


# Определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']


def scrapping_habr():
    headers = Headers(browser='chrome', os='win').generate()
    response = requests.get('https://habr.com/ru/all/', headers=headers)
    soup = BeautifulSoup(response.text, features='lxml')
    articles = soup.find_all('article', class_='tm-articles-list__item')

    all_articles = []
    for article in articles:
        title = article.find('a', class_='tm-title__link')
        link = 'https://habr.com' + title['href']

        time = article.find('time')['datetime']
        date_formatted = datetime.fromisoformat(time).strftime('%d.%m.%Y %H:%M')

        preview = article.find('div', class_='article-formatted-body')
        if preview:
            text_preview = preview.text.strip().lower()
        else:
            preview = article.find('div', class_='tm-article-body')
            text_preview = preview.text.strip().lower() if preview else ''

        tags = article.find_all('a', class_='tm-tags-list__link')
        text_tags = ' '.join([tag.text.strip().lower() for tag in tags])

        hubs = article.find_all('a', class_='tm-hubs-list__link')
        text_hubs = ' '.join([hub.text.strip().lower() for hub in hubs])

        all_text = f"{title.text.strip().lower()} {text_preview} {text_tags} {text_hubs}"

        found_keywords = [keyword for keyword in KEYWORDS if keyword.lower() in all_text]

        if found_keywords:
            all_articles.append({
                'date': date_formatted,
                'title': title,
                'link': link,
                'keywords': found_keywords
            })

            print(f"{date_formatted} – {title} – {link}")
            print(f"  Найдены ключевые слова: {', '.join(found_keywords)}")
            print()

    print("-" * 80)
    print(f"Всего найдено подходящих статей: {len(all_articles)}")


def main():
    scrapping_habr()

if __name__ == "__main__":
    main()