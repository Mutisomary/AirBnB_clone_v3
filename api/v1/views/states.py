#!/usr/bin/python3
"""This modules defines states Objects"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves a list of all State objects.

    Returns:
        A JSON response with a list of State objects.
    """
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object by its ID.

    Args:
        state_id (str): The ID of the State object to retrieve.

    Returns:
        A JSON response with the State object if found, or a 404 error
        if not found.
    """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object by its ID.

    Args:
        state_id (str): The ID of the State object to delete.

    Returns:
        A JSON response with an empty dictionary and a 200 status code
        if deleted, or a 404 error if not found.
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a new State object.

    Request JSON Data:
        {
            "name": "State Name"
        }

    Returns:
        A JSON response with the new State object and a 201 status code
        if created, or a 400 error with an error message if the request
        is invalid.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object by its ID.

    Args:
        state_id (str): The ID of the State object to update.

    Request JSON Data:
        {
            "key1": "value1",
            "key2": "value2",
            ...
        }

    Returns:
        A JSON response with the updated State object and a 200 status
        code if updated, or a 404 error if the State object is not found,
        or a 400 error if the request is invalid.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
