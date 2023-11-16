#!/usr/bin/python3
"""My routes"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """Return a JSON with status: OK"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """Retrieve the number of each objects by type"""
    return jsonify({
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    })
