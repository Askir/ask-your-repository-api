"""
Handles all logic of the user api
"""
from flask import jsonify, make_response
from neomodel import exceptions
from flask_jwt_extended import (jwt_required, create_access_token, unset_jwt_cookies,
                                set_access_cookies, get_csrf_token)
from webargs.flaskparser import use_args

from .application_controller import ApplicationController
from ..models.user import User
from ..responders import respond_with, no_content
from ..validators import users_validator
from ..extensions import bcrypt

class UsersController(ApplicationController):
    """ Controller for users """

    @jwt_required
    def show(self, object_id):
        try:
            user = User.find_by(id_=object_id)
            return respond_with(user), 200
        except User.DoesNotExist:  # pylint:disable=no-member
            return {"error": "not found"}, 404

    @jwt_required
    @use_args(users_validator.index_args())
    def index(self, params):  # pylint: disable=W0613
        """Logic for querying several users"""
        users = User.all()
        return {"users": respond_with(users)}, 200

    @use_args(users_validator.create_args())
    def create(self, params):
        """Logic for creating a user"""
        try:
            user = User(**params).save()
        except exceptions.UniqueProperty:
            return {"error": "Username or Email already taken"}, 409
        return respond_with(user), 200

    @jwt_required
    @use_args(users_validator.update_args())
    def update(self, params, object_id):
        """Logic for updating a user"""
        object_id = params.pop("id")
        try:
            user = User.find_by(id_=object_id)
            user.update(**params)
            return respond_with(user), 200
        except User.DoesNotExist:  # pylint:disable=no-member
            return {"error": "not found"}, 404

    @jwt_required
    @use_args(users_validator.delete_args())
    def delete(self, params, object_id):
        """Logic for deleting a user"""
        object_id = params["id"]
        try:
            user = User.find_by(id_=object_id)
            user.delete()
            return no_content()
        except User.DoesNotExist:  # pylint:disable=no-member
            return {"error": "not found"}, 404

    @use_args(users_validator.login_args())
    def login(self, params):
        """ Returns a cookie and a csrf token for double submit CSRF protection. """
        user = (User.find_by(username=params["email_or_username"], force=False)
                or User.find_by(email=params["email_or_username"], force=False))
        if not user or not bcrypt.check_password_hash(user.password, params["password"]):
            return {"error": "Bad username or password"}, 401
        access_token = create_access_token(identity=user.id_)
        response = respond_with(user)
        response["token"] = get_csrf_token(access_token)
        response = jsonify(response)
        set_access_cookies(response, access_token, 1000000)
        response = make_response(response, 200)
        response.mimetype = 'application/json'

        return response

    @jwt_required
    def logout(self): # pylint: disable=W0613
        """ Unsets the cookie in repsponse """
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        response = make_response(resp, 200)
        response.mimetype = 'application/json'
        return response