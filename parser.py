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
                post = Cinema(name=name, year=films[0], country=films[1], producer=films[2], genre=films[3],
                              duration=films[4],
                              rating=films[5], theaters=films[6], dates=films[7], time=films[8], description=films[9],
                              image=films[10])
                db.session.add(post)
                db.session.commit()
            except IntegrityError:
                print(f"Фильм {name} уже в базе данных.")

parser('Movie_sessions_parser.json')