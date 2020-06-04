import requests
from bs4 import BeautifulSoup as BS, NavigableString
import re
import json

r = requests.get('https://kino-teatr.ua/afisha-kino-kiev.phtml')
soup = BS(r.text, 'html.parser')
films = dict()
link = soup.select('div.uk-width-2-3 > a')
all_space = r'\s+'


def link_parser(link):
    links = []
    for link_search in link:
        links.append(link_search.get('href'))
    return links


def movie_theaters(movie):
    movie_info = []
    for link_session in movie:
        if link_session.text == 'Сеансы':
            r = requests.get(link_session.get('href'))
            soup = BS(r.text, 'html.parser')
            for cinema in soup.body:
                if isinstance(cinema, NavigableString):
                    continue
                if cinema.select_one('h2.uk-h4') is None:
                    continue
                movie_info.append(cinema.select('h2.uk-h4')[1].get_text(strip=True))
                movie_info.append(sessions(cinema.select('div.uk-grid.uk-grid-collapse')))
    return movie_info


def sessions(session):
    session_info = []
    for session_parser in session:
        if session_parser.select_one('div.uk-width-expand') is None:
            continue
        date_session = session_parser.select_one('div.uk-width-expand').get_text(strip=True)
        if '.' in date_session:
            session_info.append(date_session)
        if session_parser.select_one('span.uk-text-emphasis') is not None:
            session_info.append(session_parser.select_one('span.uk-text-emphasis').text)
    return session_info


for list_open in link_parser(link):
    genre_list = []
    r = requests.get(list_open)
    soup = BS(r.text, 'html.parser')
    description = soup.select_one('div.uk-width-1-1.uk-margin-small-top.tm-lh.tm-fa > p').get_text(strip=True)
    for film_parse in soup.body:
        if isinstance(film_parse, NavigableString):
            continue
        if film_parse.article is not None:
            for body_parse in film_parse.article:
                if isinstance(body_parse, NavigableString):
                    continue
                # поиск названия кинотеатра
                if body_parse.select_one('div.tm-mr > a.uk-button.uk-button-text') is not None:
                    theaters = movie_theaters(body_parse.select('div.tm-mr > a.uk-button.uk-button-text'))
                # поиск картинки фильма
                if body_parse.select_one('img.uk-width-1-1.uk-box-shadow-small') is not None:
                    image = body_parse.select_one('img.uk-width-1-1.uk-box-shadow-small').get('src')
                if body_parse.select_one('h1.uk-h2.uk-text-uppercase > span') is not None:
                    film_name = body_parse.select_one('h1.uk-h2.uk-text-uppercase > span').text
                    films.setdefault(film_name, {})
                if body_parse.select_one('div.uk-flex-last.tm-lh') is not None:
                    for a in body_parse.select('div.uk-flex-last.tm-lh > a'):
                        if '.' not in a.text:
                            if a.text.isdigit():
                                films[film_name].setdefault('year', a.text)
                            else:
                                films[film_name].setdefault('country', a.text)

                    films[film_name].setdefault('producer',
                                                body_parse.select('div.uk-flex-last.tm-lh > span > a')[0].text)
                    for genre in body_parse.select('div.uk-flex-last.tm-lh > span > a')[1:]:
                        # заполнение списка жанрами.
                        genre_list.append(genre.text)

                    # объект по которому идет поиск.
                    body = body_parse.select_one('div.uk-flex-last.tm-lh')
                    # поиск продолжительности
                    duration = re.sub(all_space, ' ', re.findall(r'Продолжительность:\s+\d+ мин.', body.text)[0])
                    # поик рейтинга
                    rating = re.sub(all_space, ' ', re.findall(r'Рейтинг IMDB:\s+[\d|.|/]+', body.text)[0])
                    # заполнение словаря выше перечисленным
                    films[film_name].setdefault('duration', duration)
                    films[film_name].setdefault('rating', rating)
                    # заполнение словаря названием кинотеатров
                    films[film_name].setdefault('theaters', theaters[0])
                    # заполнение словаря сеансами
                    # дата сеансов
                    films[film_name].setdefault('dates', theaters[1][0])
                    # время сеансов
                    try:
                        films[film_name].setdefault('time', theaters[1][1])
                    except IndexError:
                        films[film_name].setdefault('time', 'нет сеансов')
                    films[film_name].setdefault('description', description)
                    # заполнение словаря ссылкой на картинку фильма
                    films[film_name].setdefault('image', image)
    # заполнение словаря жанрами
    films[film_name].setdefault('genre', ''.join([genre_list[i] + ', ' if i != len(genre_list) - 1 else genre_list[i] for i in
                                          range(len(genre_list))]))

for i in films.items():
    print(i)

with open('Movie_sessions_parser.json', 'w', encoding='UTF-8') as f:
    json.dump(films, f, ensure_ascii=False)
