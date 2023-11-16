#!/usr/bin/python3
""" Module to handle cities APi routes"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_state_cities(state_id):
    """
    Retrieves a list of all City objects of a State.

    Args:
        state_id (str): The ID of the State for which to retrieve cities.

    Returns:
        A JSON response with a list of City objects.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = state.cities
    return jsonify([city.to_dict() for city in cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object by its ID.

    Args:
        city_id (str): The ID of the City object to retrieve.

    Returns:
        A JSON response with the City object if found
        or a 404 error if not found.
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object by its ID.

    Args:
        city_id (str): The ID of the City object to delete.

    Returns:
        A JSON response with an empty dictionary and a 200 status code
        if deleted or a 404 error if the City object is not found.
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a new City object for a given State.

    Args:
        state_id (str): The ID of the State for which to create a City.

    Request JSON Data:
        {
            "name": "City Name"
        }

    Returns:
        A JSON response with the new City object and a 201 status code
        if created, or a 404 error if the State is not found,
        or a 400 error with an error message if the request is invalid.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    new_city = City(**data)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Updates a City object by its ID.

    Args:
        city_id (str): The ID of the City object to update.

    Request JSON Data:
        {
            "key1": "value1",
            "key2": "value2",
            ...
        }

    Returns:
        A JSON response with the updated City object and a 200 status code
        if updated, or a 404 error if the City object is not found,
        or a 400 error with an error message if the request is invalid.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())
