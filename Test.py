from app import db, models
import datetime

# u = models.User(nickname = "Susan", email = "Susan@gmail.com", role = models.ROLE_USER)
# db.session.add(u)
# db.session.commit()
users = models.User.query.all()
for u in users:
	print(u.id, u.nickname, u.email)
u = models.User.query.get(1)
p = models.Post(body='my first post!', timestamp=datetime.datetime.utcnow(), author=u)

s = models.User.query.get(2)
print(s.posts.all())

