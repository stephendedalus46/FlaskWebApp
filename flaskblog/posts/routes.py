from flask import render_template  # function for returning HTML in the function
from flask import url_for  # if there is a change in the root URL then you have to change it in every page where the link is present
from flask import flash  # popup message
from flask import redirect  # function for redirection to another rout
from flask import request  # to access requests from urls
from flask import abort  # to indispose to update not user's post
from flask import Blueprint

from flask_login import current_user  # to disable possibility to go to login/register route when user is logged in
from flask_login import login_required  # to disable access to account route while logout

from flaskblog import db  # variables(instances of classes) from __init__
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm  # class defined by me

posts = Blueprint('posts', __name__)  # similar to creating flask object, users is name of blueprint


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route('/post/<int:post_id>')  # variable in route, int - expecting integer
def post(post_id):
    post = Post.query.get_or_404(post_id)  # get_or_404 if page doesn't exist send 404, if does render template
    return render_template('post.html', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])  # variable in route, int - expecting integer
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)  # get_or_404 if page doesn't exist send 404, if does render template
    if post.author != current_user:
        abort(403)  # 403 stands for forbidden route, abort needs to be imported from flask
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()  # no need to add db, because it's only update, so posts are already id db
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')  # legend added to avoid need of creating new template just for different legend comparing to createpost template


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)  # get_or_404 if page doesn't exist send 404, if does render template
    if post.author != current_user:
        abort(403)  # 403 stands for forbidden route, abort needs to be imported from flask
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
