from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from models import BlogPost, BlogComment, db
from blog_posts.forms import BlogPostForm
from blog_posts.forms import BlogCommentForm

blog_posts = Blueprint('blog_posts', __name__)

#CREATE BLOG POSTS
@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():

        blog_post = BlogPost(title=form.title.data,
                            text=form.text.data,
                            user_id=current_user.id)
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created')
        return redirect(url_for('core.index'))

    return render_template('create_post.html', form=form)


#BLOG POST(VIEW)
@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    blog_comments = blog_post.comments
    print(blog_comments)
    return render_template('blog_post.html', title=blog_post.title,
                            date=blog_post.date, post=blog_post, blog_comments=blog_comments)

# @blog_posts.route('/<int:blog_post_id>/<int:blog_comment_id>')
# def blog_post_with_comments(blog_post_id, blog_comment_id):
#     blog_post = BlogPost.query.get_or_404(blog_post_id)
#     blog_comment = BlogComment.query.get_or_404(blog_comment_id)
#     return render_template('blog_post_with_comments.html', title=blog_post.title,
#                             date=blog_post.date, post=blog_post, comment=blog_comment)


#UPDATE
@blog_posts.route('/<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    form = BlogPostForm()


    if form.validate_on_submit():

        blog_post.title = form.title.data
        blog_post.text = form.text.data,
        db.session.commit()
        flash('Blog Post Updated')
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))

    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text

    return render_template('create_post.html', title='Updating', form=form)

#DELETE
@blog_posts.route('/<int:blog_post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(blog_post_id):

    blog_post = BlogPost.query.get_or_404(blog_post_id)
    blog_comments = blog_post.comments
    if blog_post.author != current_user:
        abort(403)


    for blog_comment in blog_comments:
        db.session.delete(blog_comment)

    print("test"*50, blog_comments)
    print("test"*50, blog_post)
    

    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog Post Deleted')
    return redirect(url_for('core.index'))

#COMMENT
@blog_posts.route('/<int:blog_post_id>/comment', methods=['GET', 'POST'])
@login_required
def create_comment(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    form = BlogCommentForm()

    if form.validate_on_submit():

        blog_comment = BlogComment(comment=form.comment.data,
                                    user_id=current_user.id,
                                    blog_post_id=blog_post_id)
        db.session.add(blog_comment)
        db.session.commit()
        flash('Comment Successfully!')
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))

    return render_template('create_comment.html', form=form)
