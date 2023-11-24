from notesfromkatieland import createApp, db
from notesfromkatieland.models import AllowedUser, User, Post, Video

app = createApp()
app.app_context().push()
db.create_all()

VALID_LOCATIONS = ['New_York', 'Milwaukee', 'Madison', 'Chicago']

users = User.query.all()
for user in users:
    if user.location == 'xxxx':
        userData = AllowedUser.query.filter_by(email=user.email).first()
        user.location = userData.placeDefault
        print(f'Updated user with email {user.email} to location {user.location}.')
db.session.commit()

posts = Post.query.all()
for post in posts:
    assert post.author.location in VALID_LOCATIONS, 'Author has an invalid location'
    if post.location == 'xxxx':
        post.location = post.author.location
        print(f'Updated post with title {post.title} to location {post.location}.')
db.session.commit()

videos = Video.query.all()
for video in videos:
    assert video.author.location in VALID_LOCATIONS, 'Author has an invalid location'
    if video.location == 'xxxx':
        video.location = video.author.location
        print(f'Updated video with title {video.title} to location {video.location}.')
db.session.commit()