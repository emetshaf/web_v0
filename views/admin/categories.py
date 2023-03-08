from flask import render_template, request, redirect
import json
import os
import requests
from uuid import uuid4
from web.views.admin import admin_views
from web.views.common import api_status, allowed_file, UPLOAD_FOLDER, get_username


@ admin_views.route('/categories', strict_slashes=False)
def admin_categories():
    """Admin Categories Management Page
    """
    if api_status()['status'] == 'OK':
        if get_username() is None:
            return redirect('/admin/signin')
        url = "http://localhost/api/v1/categories"
        categories = requests.get(url).json()
        subcategories = requests.get(
            "http://localhost/api/v1/subcategories").json()
        cache_id = uuid4()
        return render_template(
            'admin/categories.html',
            categories=categories,
            subcategories=subcategories,
            segment='categories',
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@admin_views.route('/edit_category/<category_id>', methods=['GET', 'POST'], strict_slashes=False)
def edit_category(category_id):
    """Admin Edit Category Page
    """
    if api_status()['status'] == 'OK':
        url = "http://localhost/api/v1/categories/" + category_id
        category = requests.get(url).json()
        if request.method == 'POST':
            url = "http://localhost/api/v1/categories/" + category_id
            name = request.form['name']
            payload = {
                'name': name
            }
            requests.put(url, json=payload)
            return redirect('/admin/categories')
        cache_id = uuid4()
        return render_template(
            'admin/edit_category.html',
            category=category,
            cache_id=cache_id,
        )
    else:
        return render_template(
            '500.html',
            cache_id=cache_id,
        )


@ admin_views.route('/create_category', methods=['POST'], strict_slashes=False)
def create_category():
    if request.method == 'POST':
        url = "http://localhost/api/v1/categories/"
        name = request.form['name']
        payload = {
            'name': name
        }
        requests.post(url, json=payload)
        return redirect('/admin/categories')


@admin_views.route('/create_subcategory', methods=['POST'], strict_slashes=False)
def create_subcategory():
    if request.method == 'POST':
        url = "http://localhost/api/v1/subcategories/"
        name = request.form['name']
        category_id = request.form['category_id']
        payload = {
            'name': name,
            'category_id': category_id
        }
        requests.post(url, json=payload)
        return redirect('/admin/categories')


@ admin_views.route('/delete_category/<category_id>', strict_slashes=False)
def delete_category(category_id):
    url = "http://localhost/api/v1/categories/" + category_id
    requests.delete(url)
    return redirect('/admin/categories')
