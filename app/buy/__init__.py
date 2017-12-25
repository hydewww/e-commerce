from flask import Blueprint

buy = Blueprint('buy', __name__)

from . import views
