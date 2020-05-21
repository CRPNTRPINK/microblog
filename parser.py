import json
from app import db
from sqlalchemy.exc import IntegrityError
from app.models import Cinema


def parser(name):
    with open(name, encoding='UTF-8') as f:
        js = json.load(f)
        for name in js:
            films = list(js[name].values())
            try:
                post = Cinema(name=name, year=films[0], country=films[1], producer=films[2], duration=films[3],
                              rating=films[4],
                              theaters=films[5], dates=films[6], time=films[7], description=films[8], image=films[9],
                              genre=films[10])
                db.session.add(post)
                db.session.commit()
            except IntegrityError:
                print(f"Фильм {name} уже в базе данных.")

parser('Movie_sessions_parser.json')