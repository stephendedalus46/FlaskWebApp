from flask import render_template  # function for returning HTML in the function
from flask import request  # to access requests from urls
from flask import Blueprint

from flaskblog.models import Post

main = Blueprint('main', __name__)  # similar to creating flask object, users is name of blueprint


@main.route('/')  # / stands for root page of website/homepage
@main.route('/home')  # one function handles two routes
def home():
    page = request.args.get('page', 1, type=int)  # default page = 1
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)  # we don't want to have all() on one page, order_by -> newest on top
    return render_template('home.html', posts=posts)  # passing also list from code


@main.route('/about')
def about():
    return render_template('about.html', title='About')