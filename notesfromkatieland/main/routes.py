from flask import render_template, request, Blueprint
from flask_login import login_required
from notesfromkatieland.models import Post

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/testimonials')
@login_required
def testimonials():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.datePosted.desc()).paginate(page=page, per_page=5)
    return render_template('testimonials.html', posts=posts)

@main.route('/videos')
@login_required
def videos():
    return render_template('videos.html', title='Videos')

@main.route('/games')
@login_required
def games():
    return render_template('games.html', title='Games')