from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from notesfromkatieland import db
from notesfromkatieland.models import Post
from notesfromkatieland.posts.forms import PostForm
from notesfromkatieland.posts.utils import savePicture

posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def newPost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        if form.picture.data:
            imageFilename = savePicture(form.picture.data)
            post.imageFile = imageFilename
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.testimonials'))
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
        print(form.picture.data)
        if form.picture.data:
            imageFilename = savePicture(form.picture.data)
            print(imageFilename)
            post.imageFile = imageFilename
        print(post.title, post.content, post.imageFile)
        db.session.commit()
        flash('Post updated!', 'success')
        return redirect(url_for('posts.post', postID=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('newPost.html', title='Update Post', form=form, legend='Update Post')

@posts.route('/post/<int:postID>/delete', methods=['POST'])
@login_required
def deletePost(postID):
    post = Post.query.get_or_404(postID)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'success')
    return redirect(url_for('main.testimonials'))