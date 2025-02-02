#!/usr/bin/python3
"""Module places.py: contains users information"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.review import Review
from models.user import User
from models.place import Place
from models import storage


@app_views.route('reviews/<review_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def review(review_id):
    """returns an review based on it's id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if request.method == 'DELETE':
        review.delete()
        storage.save()
        return '{}'

    if request.method == 'PUT':
        res = request.get_json()
        if res is None:
            abort(400, description='Not a JSON')
        for k, v in res.items():
            if k.endswith('ed_at') or k.endswith('id'):
                continue
            setattr(review, k, v)
        review.save()

    return jsonify(review.to_dict())


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def reviews(place_id):
    """displays and creates an review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'POST':
        res = request.get_json()
        if res is None:
            abort(400, description='Not a JSON')
        if 'text' not in res.keys():
            abort(400, description='Missing text')
        if 'user_id' not in res.keys():
            abort(400, description='Missing user_id')

        user = storage.get(User, res['user_id'])
        if user is None:
            abort(404)
        res['place_id'] = place.id
        new_review = Review(**res)
        new_review.save()
        return jsonify(new_review.to_dict()), 201

    review = [v.to_dict() for v in place.reviews]
    return jsonify(review)
