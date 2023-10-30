from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from notesfromkatieland import db
from notesfromkatieland.models import Video
from notesfromkatieland.videos.forms import VideoForm
from notesfromkatieland.videos.utils import saveVideo

videos = Blueprint('videos', __name__)

@videos.route('/video/new', methods=['GET', 'POST'])
@login_required
def newVideo():
    form = VideoForm()
    if form.validate_on_submit():
        videoFilename = saveVideo(form.video.data)
        video = Video(title=form.title.data, videoFile=videoFilename, author=current_user)
        db.session.add(video)
        db.session.commit()
        flash('Your video has been created!', 'success')
        return redirect(url_for('main.videos'))
    return render_template('newVideo.html', title='New Video', form=form, legend='New Video')

@videos.route('/video/<int:videoID>')
@login_required
def video(videoID):
    video = Video.query.get_or_404(videoID)
    return render_template('video.html', title=video.title, video=video)

@videos.route('/video/<int:videoID>/update', methods=['GET', 'POST'])
@login_required
def updateVideo(videoID):
    video = Video.query.get_or_404(videoID)
    if video.author != current_user:
        abort(403)

    form = VideoForm()
    if form.validate_on_submit():
        video.title = form.title.data
        video.videoFile = saveVideo(form.video.data)
        db.session.commit()
        flash('Video updated!', 'success')
        return redirect(url_for('videos.video', videoID=video.id))
    elif request.method == 'GET':
        form.title.data = video.title
        form.video.data = video.videoFile
    return render_template('newVideo.html', title='Update Video', form=form, legend='Update Video')

@videos.route('/video/<int:videoID>/delete', methods=['POST'])
@login_required
def deleteVideo(videoID):
    video = Video.query.get_or_404(videoID)
    if video.author != current_user:
        abort(403)

    db.session.delete(video)
    db.session.commit()
    flash('Video deleted.', 'success')
    return redirect(url_for('main.videos'))