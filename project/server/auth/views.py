from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, db
from project.server.models import User

auth_blueprint = Blueprint( 'auth', __name__ )

class RegisterAPI( MethodView ):
    """
    User Registration Resource
    """

    def post( self ):
        #get post data
        post_data = request.get_json()

        #check valid new user request
        user = User.query.filter_by( email=post_data.get( 'email' ) ).first()
        if not user:#valid new user
            try:
                user = User(
                    email=post_data.get( 'email' ),
                    password=post_data.get( 'password' )
                )

                #store the user
                db.session.add( user )
                db.session.commit()

                #generate auth token for auth on registration
                #questionable
                auth_token = user.encode_auth_token( user.id )
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully refistered.',
                    'auth_token':auth_token.decode()
                }
                #TODO research this interesting syntax
                return make_response( jsonify( responseObject ) ), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Error occurrred.',
                }
                #TODO research this interesting syntax
                return make_response( jsonify( responseObject ) ), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User not available',
            }
            #TODO research this interesting syntax
            return make_response( jsonify( responseObject ) ), 202

#define API resource
registration_view = RegisterAPI.as_view( 'register_api' )

#add rules and API endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=[ 'POST' ]
)
