
from http import HTTPStatus

from flask import request
from flask_restful import Resource, abort
from flasgger import swag_from

from shorten_url import exc
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

        return {"id": user_id}, HTTPStatus.CREATED.value

    @swag_from("swagger/users/get.yml", validation=False)
    def get(self):
        """ List the users
        input:
            offset (optional)
            limit (optional)
        output:
            list of users
        """
        try:
            args = request.args
            page = int(args.get('user_id', 0))
            page_size = int(args.get('user_size', 100))

        except Exception as e:
            LOGGER.info(f"invalid args:{e}")
            return abort(HTTPStatus.BAD_REQUEST.value,
                         message=HTTPStatus.BAD_REQUEST.description)

        try:
            users = USER_USECASE.list_users(page, page_size)
        except Exception as e:
            LOGGER.error(f"internal server error:{e}")
            return abort(HTTPStatus.INTERNAL_SERVER_ERROR.value,
                         message=HTTPStatus.INTERNAL_SERVER_ERROR.description)

        return users, HTTPStatus.OK.value


# /shorten_url/v1/user/
class User(Resource):

    @swag_from("swagger/user/delete.yml", validation=False)
    def delete(self, user_id):
        """ Delete the user
        input:
            user_id (in the routing path)
        output:
            none
        """
        try:
            USER_USECASE.delete_user(user_id)
        except Exception as e:
            LOGGER.error(f"internal server error:{e}")
            return abort(HTTPStatus.INTERNAL_SERVER_ERROR.value,
                         message=HTTPStatus.INTERNAL_SERVER_ERROR.description)

        return HTTPStatus.OK.value

    @swag_from("swagger/user/get.yml", validation=False)
    def get(self, user_id):
        """ Lit the user infomation
        """
        try:
            user = USER_USECASE.get_user_info(user_id)
        except exc.NoUserFoundError as e:
            LOGGER.info(f":{e}")
            return abort(HTTPStatus.NOT_FOUND.value,
                         message=HTTPStatus.NOT_FOUND.description)
        except Exception as e:
            LOGGER.error(f"internal server error:{e}")
            return abort(HTTPStatus.INTERNAL_SERVER_ERROR.value,
                         message=HTTPStatus.INTERNAL_SERVER_ERROR.description)

        return user, HTTPStatus.OK.value
