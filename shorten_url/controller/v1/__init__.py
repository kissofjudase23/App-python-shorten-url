from flask import Blueprint
from flask_restful import Api

from shorten_url.controller.v1.user import Users, User
from shorten_url.controller.v1.url import Urls, Url, UrlRedirect

api_bp = Blueprint("api_v1", __name__)
api = Api(api_bp)
api.add_resource(Users, "/users")
api.add_resource(User, "/users/<user_id>")
api.add_resource(Urls, "/users/<user_id>/urls")
api.add_resource(Url, "/users/<user_id>/urls/<url_id>")
api.add_resource(UrlRedirect, "/<url_id>")
