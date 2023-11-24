from flask import render_template, request, Blueprint
from flask_login import login_required
from notesfromkatieland.models import Post, Video

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/testimonials')
@login_required
def testimonials():
    return render_template('landing.html', opt='Testimonials', route='main.placeTestimonials')

@main.route('/testimonials/<string:place>')
def placeTestimonials(place):
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(location=place).order_by(Post.datePosted.desc()).paginate(page=page, per_page=5)
    return render_template('testimonials.html', place=place.replace('_', ' '), posts=posts)

@main.route('/videos')
@login_required
def videos():
    return render_template('landing.html', opt='Videos', route='main.placeVideos')

@main.route('/videos/<string:place>')
def placeVideos(place):
    page = request.args.get('page', 1, type=int)
    videos = Video.query.filter_by(location=place).order_by(Video.datePosted.desc()).paginate(page=page, per_page=5)
    return render_template('videos.html', place=place.replace('_', ' '), videos=videos)