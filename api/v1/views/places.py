#!/usr/bin/python3
"""Module users.py: contains users information"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route('places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place(place_id):
    """returns an place based on it's id"""
    place = storage.get(Place, place_id)
    if place is none:
        abort(404)

    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return '{}'

    if request.method == 'PUT':
        res = request.get_json()
        if res is None:
            abort(400, description='Not a JSON')
        for k, v in res.items():
            if k.endswith('ed_at') or k.endswith('id'):
                continue
            setattr(place, k, v)
        place.save()

    return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def places(city_id):
    """displays and creates an place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'POST':
        res = request.get_json()
        if res is None:
            abort(400, description='Not a JSON')
        if 'name' not in res.keys():
            abort(400, description='Missing name')
        if 'user_id' not in res.keys():
            abort(400, description='Missing user_id')

        user = storage.get(User, res['user_id'])
        if user is None:
            abort(404)
        res['city_id'] = city.id
        new_place = Place(**res)
        new_place.save()
        return jsonify(new_place.to_dict()), 201

    places = [v.to_dict() for v in storage.all(Place).values()
             if v.city_id == city_id]
    return jsonify(places)

