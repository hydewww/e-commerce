from flask import Blueprint

sell = Blueprint('sell', __name__)

from . import views
