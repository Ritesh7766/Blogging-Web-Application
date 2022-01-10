from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login  import current_user, login_required
from include import db
from include.models import Post
from include.posts.forms import NewPost


posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def post():
    form = NewPost()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data,  content=form.content.data, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash('Post uploaded successfully!', category='success')
        return redirect(url_for('main.index'))
    return render_template('post.html', form=form, Legend='New Post')


@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('get_post.html', post=post)


@posts.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', category='success')
    return redirect(url_for('main.index'))


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = NewPost() 
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated successfully!', category='success')
        return redirect(url_for('posts.get_post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('post.html', form=form, post=post, Legend='Update Post')