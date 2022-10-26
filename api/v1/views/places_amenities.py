#!/usr/bin/python3
"""Module places_amenities.py: contains amenity information"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.place import Place
from models.amenity import Amenity
from models import storage
import os


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'],
                 strict_slashes=False)
def place_amenities(place_id):
    """displays all amenities to a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = place.amenities
    else:
        amenities = place.amenity_ids

    result = [i.to_dict() for i in amenities]
    return jsonify(result)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'],
                 strict_slashes=False)
def place_amenity(place_id, amenity_id):
    """deletes or clinks amenity to a place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None or place is None:
        abort(404)

    if os.getenv("HBNB_TYPE_STORAGE") == 'db':
        amenities = place.amenities
    else:
        amenities = place.amenity_ids

    if request.method == 'POST':
        if amenity in amenities:
            return jsonify(amenity.to_dict())
        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201

    if amenity not in amenities:
        abort(404)
    place.amenities.remove(amenity)
    place.save()
    return '{}'
