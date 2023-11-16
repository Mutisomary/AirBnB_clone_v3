#!/usr/bin/python3
""" My views funnctions """
from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Wildcard import of everything in the package api.v1.views.index
from api.v1.views.index import *
from .states import *
from api.v1.views import cities
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
