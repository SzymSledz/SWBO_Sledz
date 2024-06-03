from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from pjf import db
from pjf.models import articles
from datetime import datetime


article = Blueprint('article', __name__)

@article.route('/article')
def article_page():
    all_articles = articles.query.all()
    return render_template('article.html', articles=all_articles)

@article.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if 'login' in session and session['login'] == 'admin':
        if request.method == 'POST':
            title = request.form['title']
            text = request.form['text']
            new_article = articles(title=title, date=datetime.now(), text=text)
            db.session.add(new_article)
            db.session.commit()
            flash('Article added successfully!', 'success')
            return redirect(url_for('article.article_page'))
        return render_template('add_article.html')
    else:
        flash('You must be logged in as admin to add articles.', 'danger')
        return redirect(url_for('article.article_page'))