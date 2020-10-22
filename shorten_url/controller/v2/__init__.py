from flask import Blueprint
from flask_restful import Api


api_bp = Blueprint("api_v2", __name__)
api = Api(api_bp)
