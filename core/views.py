from models import BlogPost
from flask import render_template, request, Blueprint, flash, redirect, url_for
from datetime import datetime
from blog_posts.forms import BlogPostForm
from flask_login import current_user, login_required
from models import BlogPost, db


core = Blueprint('core', __name__)

@core.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = BlogPostForm()

    if form.validate_on_submit():

        blog_post = BlogPost(title=form.title.data,
                            text=form.text.data,
                            user_id=current_user.id)
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created')
        return redirect(url_for('core.index'))

    page = request.args.get('page',1,type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)

    return render_template('index.html',blog_posts=blog_posts, form=form)


@core.route('/info')
def info():
    return render_template('info.html')
