
from http import HTTPStatus

from flask import request, Response
from flask_restful import Resource, abort
from flasgger import swag_from

from shorten_url import exc
from shorten_url.controller import make_json_response
from shorten_url.storages import Repositories
from shorten_url.cache import get_cache
from shorten_url.usecases.user import User as user_usecase
from shorten_url.logger import LogFactory


USER_REPO = Repositories.user()
CACHE = get_cache()
USER_USECASE = user_usecase(USER_REPO, CACHE)
LOGGER = LogFactory.logger(name=__name__)


# /shorten_url/v1/users/
class Users(Resource):
    @swag_from("swagger/users/post.yml", validation=False)
    def post(self):
        """ Creat a new user
        input:
            email
            name
        output:
            user_id
        """
        try:
            body = request.get_json()
            name = body.get("name").lower()
            email = body.get("email").lower()
        except Exception as e:
            LOGGER.info(f"invalid args:{e}")
            return abort(HTTPStatus.BAD_REQUEST.value,
                         message=HTTPStatus.BAD_REQUEST.description)

        try:
            user_id = USER_USECASE.add_user(name, email)
        except exc.DuplicateUserError as e:
            LOGGER.info(f"conflict error:{e}")
            return abort(HTTPStatus.CONFLICT.value,
                         message=f"conflict email:{email}")

        except Exception as e:
            LOGGER.error(f"internal server error:{e}")
            return abort(HTTPStatus.INTERNAL_SERVER_ERROR.value,
                         message=HTTPStatus.INTERNAL_SERVER_ERROR.description)

        return make_json_response({"user_id": user_id},
                                  HTTPStatus.CREATED.value)

    def get(self):
        """ List the users
        input:
            offset (optional)
            limit (optional)
        output:
            list of users
        """
        try:
            users = USER_USECASE.list_users()
        except Exception as e:
            LOGGER.error(f"internal server error:{e}")
            return abort(HTTPStatus.INTERNAL_SERVER_ERROR.value,
                         message=HTTPStatus.INTERNAL_SERVER_ERROR.description)

        return make_json_response({users}, 200)


# /shorten_url/v1/user/
class User(Resource):
    def delete(self, user_id):
        """ Delete the user
        input:
            user_id (in the routing path)
        output:
            none
        """
        try:
            user_id = request.args.get('user_id').lower()
        except KeyError as e:
            LOGGER.info(f"invalid args:{e}")
            return abort(HTTPStatus.BAD_REQUEST.value,
                         message=HTTPStatus.BAD_REQUEST.description)

        try:
            USER_USECASE.delete_user(user_id)
        except Exception as e:
            LOGGER.error(f"internal server error:{e}")
            return abort(HTTPStatus.INTERNAL_SERVER_ERROR.value,
                         message=HTTPStatus.INTERNAL_SERVER_ERROR.description)

        return Response(status=200)

    # def get(self, user_id):
    #     """ Lit the user infomation
    #     """
