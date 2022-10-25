#!/usr/bin/python3
"""Module places_amenities.py: contains amenity information"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.place import Place, place_amenity
from models.amenity import Amenity
from models import storage


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'],
                 strict_slashes=False)
def place_amenities(place_id):
    """displays all amenities to a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = [v.to_dict() for v in place.amenities]
    return jsonify(amenity)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE, POST'],
                 strict_slashes=False)
def place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if request.method == 'DELETE':
        amenity.delete()
        storage.save()
        return '{}'

    result = [i for i in place.amenities if i.place_id == place_id]
    if result:
        return result[0].to_dict()
