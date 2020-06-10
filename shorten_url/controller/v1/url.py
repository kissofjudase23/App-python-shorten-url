

from flask_restful import Resource
from werkzeug.exceptions import BadRequest, InternalServerError


class Urls(Resource):
    def post(self, user_id):
        """ Creat a new shorten url
        input:
            user_id (path)
            url
        output:
            url_id (can be transfer to url)
        """

    def get(self, user_id):
        """
        need offset and limit
        """
        pass


class Url(Resource):
    def delete(self, user_id, url_id):
        """
        delete the user
        """
        pass

    def get(self, user_id, url_id):
        """
        get the url info
        """
        pass


class UrlRedirect(Resource):

    def get(self, url_id):
        """
        Redirect URL
        """
        pass
