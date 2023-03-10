from flask import render_template, request, redirect
import json
import os
import requests
from uuid import uuid4
from web.views.admin import admin_views
from web.config import api_status, allowed_file, UPLOAD_FOLDER, get_username


@ admin_views.route('/books', strict_slashes=False)
def admin_books():
    """Admin Books Management Page
    """
    cache_id = uuid4()
    if api_status()['status'] == 'OK':
        if get_username() is None:
            return redirect('/admin/signin')
        url = "http://localhost/api/v1/books"
        books = requests.get(url).json()
        authors = requests.get("http://localhost/api/v1/authors").json()
        languages = requests.get("http://localhost/api/v1/languages").json()
        categories = requests.get(
            "http://localhost/api/v1/subcategories").json()
        return render_template(
            'admin/books.html',
            books=books,
            authors=authors,
            languages=languages,
            categories=categories,
            segment='books',
            cache_id=cache_id,
        )
    return render_template('error.html', error_code='500', message='Internal Server Error', cache_id=cache_id)


@ admin_views.route('/create_book', methods=['POST'], strict_slashes=False)
def create_book():
    if request.method == 'POST':
        url = "http://localhost/api/v1/books/"
        title = request.form['title']
        fold = title.replace(" ", "_")
        folder = os.path.join(UPLOAD_FOLDER +
                              '/books/' + fold + '/')
        if not os.path.exists(folder):
            os.mkdir(folder)
        filename = ''
        covername = ''
        if 'cover' in request.files:
            cover = request.files['cover']
            if cover and allowed_file(cover.filename):
                extension = os.path.splitext(cover.filename)[1]
                covername = 'cover' + extension
                cover.save(os.path.join(
                    folder + covername))

        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                extension = os.path.splitext(file.filename)[1]
                filename = 'file' + extension
                file.save(os.path.join(
                    folder + filename))
        description = request.form['description']
        language_id = request.form['language']
        payload = {
            'cover': fold + '/' + covername,
            'title': title,
            'description': description,
            'language_id': language_id,
            'file': fold + '/' + filename,
        }
        book = requests.post(url, json=payload)
        authors = request.form.getlist('authors')
        book_id = book.json()['id']
        for author in authors:
            requests.post("http://localhost/api/v1/books/" +
                          str(book_id) + '/authors/' + author)
        categories = request.form.getlist('categories')
        for category in categories:
            requests.post("http://localhost/api/v1/books/" +
                          str(book_id) + '/categories/' + category)
        return redirect('/admin/books')


@ admin_views.route('/delete_book/<book_id>', strict_slashes=False)
def delete_book(book_id):
    url = "http://localhost/api/v1/books/" + book_id
    requests.delete(url)
    return redirect('/admin/books')
