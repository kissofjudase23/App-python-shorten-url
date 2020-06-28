from http import HTTPStatus

from flask import request
from flask_restful import Resource, abort
from flasgger import swag_from

from shorten_url import exc
from shorten_url.variables import AppVars
from shorten_url.storages import Repositories
from shorten_url.usecases.url import Url as UrlUsecases
from shorten_url.logger import LogFactory


URL_REPO = Repositories.url()
CACHE = Repositories.cache()
URL_USECASE = UrlUsecases(URL_REPO, CACHE)
LOGGER = LogFactory.logger(name=__name__)


class Urls(Resource):

    @swag_from("swagger/urls/post.yml", validation=False)
    def post(self, user_id):
        """ Creat a new shorten url
        input:
            body:
                user_id (path)
                url
        output:
            shorten_url
        """
        try:
            body = request.get_json()
            url = body.get("url").lower()
        except Exception as e:
            err_msg = f"invalid args:{e}"
            LOGGER.info(err_msg)
            return abort(HTTPStatus.BAD_REQUEST.value,
                         message=err_msg)

        try:
            url_id = URL_USECASE.add_url(user_id, url)

        except exc.NoUserFoundError:
            err_msg = f"user_id:{user_id} not found"
            LOGGER.warn(err_msg)
            return abort(HTTPStatus.NOT_FOUND.value,
                         message=err_msg)

        except exc.DuplicateUrlError:
            err_msg = f"conflict url:{url}"
            LOGGER.warn(err_msg)
            return abort(HTTPStatus.CONFLICT.value,
                         message=err_msg)

        except Exception as e:
            LOGGER.error(f"internal server error:{e}")
            return abort(HTTPStatus.INTERNAL_SERVER_ERROR.value,
                         message=HTTPStatus.INTERNAL_SERVER_ERROR.description)

        shorten_url = f"{AppVars.HOST}/shorten_url/v1/{url_id}"
        return shorten_url, HTTPStatus.CREATED.value

    @swag_from("swagger/urls/get.yml", validation=False)
    def get(self, user_id):
        """ List the urls of the user
        input:
            path:
                user_id
            args:
                page      (optional)
                page_size (optional)
        output:
            urls
        """
        try:
            args = request.args
            page = int(args.get('page', 0))
            page_size = int(args.get('page_size', 100))

        except Exception as e:
            err_msg = f"invalid args:{e}"
            LOGGER.info(err_msg)
            return abort(HTTPStatus.BAD_REQUEST.value,
                         message=err_msg)

        try:
            urls = URL_USECASE.list_urls(user_id, page, page_size)
        except Exception as e:
            LOGGER.error(f"internal server error:{e}")
            return abort(HTTPStatus.INTERNAL_SERVER_ERROR.value,
                         message=HTTPStatus.INTERNAL_SERVER_ERROR.description)

        return urls, HTTPStatus.OK.value


class Url(Resource):

    @swag_from("swagger/url/delete.yml", validation=False)
    def delete(self, user_id, url_id):
        """ delete the user
        input:
            path:
                user_id
            args:
                url_id
        output:
            urls
        """
        try:
            URL_USECASE.delete_url(user_id, url_id)
        except exc.NoUrlFoundError:
            pass
        except Exception as e:
            LOGGER.error(f"internal server error:{e}")
            return abort(HTTPStatus.INTERNAL_SERVER_ERROR.value,
                         message=HTTPStatus.INTERNAL_SERVER_ERROR.description)

        return HTTPStatus.OK.value


class UrlRedirect(Resource):

    def get(self, url_id):
        """
        Redirect URL
        """
        try:
            ori_url = URL_USECASE.get_ori_url(url_id)
        except exc.NoUrlFoundError:
            err_msg = f"url_id:{url_id} not found"
            LOGGER.warn(err_msg)
            return abort(HTTPStatus.NOT_FOUND.value,
                         message=err_msg)

        except Exception as e:
            LOGGER.error(f"internal server error:{e}")
            return abort(HTTPStatus.INTERNAL_SERVER_ERROR.value,
                         message=HTTPStatus.INTERNAL_SERVER_ERROR.description)

        return {}, HTTPStatus.FOUND.value, {"Location": ori_url}
