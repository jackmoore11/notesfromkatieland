from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from notesfromkatieland import db
from notesfromkatieland.models import Post, Picture
from notesfromkatieland.posts.forms import PostForm
from notesfromkatieland.posts.utils import savePicture

posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def newPost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, location=form.location.data, author=current_user)
        for formPicture in form.pictures.data:
            if formPicture:
                filename = savePicture(formPicture)
                picture = Picture(filename=filename, parentPost=post)
                db.session.add(picture)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.placeTestimonials', place=form.location.data))
    form.location.data = current_user.location.replace('_', ' ')
    return render_template('newPost.html', title='New Post', form=form, legend='New Post')

@posts.route('/post/<int:postID>')
@login_required
def post(postID):
    post = Post.query.get_or_404(postID)
    return render_template('post.html', title=post.title, post=post)

@posts.route('/post/<int:postID>/update', methods=['GET', 'POST'])
@login_required
def updatePost(postID):
    post = Post.query.get_or_404(postID)
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.location = form.location.data
        for formPicture in form.pictures.data:
            if formPicture:
                filename = savePicture(formPicture)
                picture = Picture(filename=filename, parentPost=post)
                db.session.add(picture)
        db.session.commit()
        flash('Post updated!', 'success')
        return redirect(url_for('posts.post', postID=post.id))
    elif request.method == 'GET':
        form.location.data = post.location.replace('_', ' ')
        form.title.data = post.title
        form.content.data = post.content
    return render_template('newPost.html', title='Update Post', form=form, legend='Update Post')

@posts.route('/post/<int:postID>/delete', methods=['POST'])
@login_required
def deletePost(postID):
    post = Post.query.get_or_404(postID)
    if post.author != current_user:
        abort(403)

    postPics = Picture.query.filter_by(parentPost=post).all()
    for pic in postPics:
        db.session.delete(pic)

    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'success')
    return redirect(url_for('main.placeTestimonials', place=post.location))