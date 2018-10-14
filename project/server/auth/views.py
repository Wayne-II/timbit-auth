#TODO: split this file based on endpoints/class
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, db
from project.server.models import User, BlacklistToken

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
					'message': 'Successfully registered.',
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
				return make_response( jsonify( responseObject ) ), 500
		else:
			responseObject = {
				'status': 'fail',
				'message': 'User not available',
			}
			#TODO research this interesting syntax
			return make_response( jsonify( responseObject ) ), 202

class LoginAPI(MethodView):
	"""
	User Login Resource
	"""
	def post(self):
		# get the post data
		post_data = request.get_json()
		try:
			# fetch the user data
			user = User.query.filter_by(
				email=post_data.get('email')
			  ).first()
			if( not user ):
				responseObject = {
					'status':'fail',
					'message':'User does not exist.'
				}
				return make_response( jsonify( responseObject ) ), 401


			if( not bcrypt.check_password_hash(
				user.password, post_data.get( 'password' )
			) ):
				responseObject = {
					'status':'fail',
					'message':'Password incorrect.'
				}
				return make_response( jsonify( responseObject ) ), 401

			auth_token = user.encode_auth_token(user.id)
			#TODO: if not auth_token
			if auth_token:
				responseObject = {
					'status': 'success',
					'message': 'Successfully logged in.',
					'auth_token': auth_token.decode()
				}
				return make_response(jsonify(responseObject)), 200
			else:
				responseObject = {
					'status':'fail',
					'message':'Error authenticating.  Contact Admin..'
				}
				return make_response( jsonify( responseObject ) ), 500
		except Exception as e:
			print(e)
			responseObject = {
				'status': 'fail',
				'message': 'Error occurrred.'
			}
			return make_response(jsonify(responseObject)), 500

class LogoutAPI(MethodView):
	"""
	Logout Resource
	"""
	def post(self):
		# get auth token
		auth_header = request.headers.get('Authorization')
		if auth_header:
			auth_token = auth_header.split(" ")[1]
		else:
			auth_token = ''
		if auth_token:
			resp = User.decode_auth_token(auth_token)
			if not isinstance(resp, str):
				# mark the token as blacklisted
				blacklist_token = BlacklistToken(token=auth_token)
				try:
					# insert the token
					db.session.add(blacklist_token)
					db.session.commit()
					responseObject = {
						'status': 'success',
						'message': 'Successfully logged out.'
					}
					return make_response(jsonify(responseObject)), 200
				except Exception as e:
					responseObject = {
						'status': 'fail',
						'message': e
					}
					return make_response(jsonify(responseObject)), 200
			else:
				responseObject = {
					'status': 'fail',
					'message': resp
				}
				return make_response(jsonify(responseObject)), 401
		else:
			responseObject = {
				'status': 'fail',
				'message': 'Provide a valid auth token.'
			}
			return make_response(jsonify(responseObject)), 403

class UserAPI(MethodView):
	"""
	User Resource
	"""
	def get(self):
		# get the auth token
		auth_header = request.headers.get('Authorization')
		if auth_header:
			try:
				auth_token = auth_header.split(" ")[1]
			except IndexError:
				responseObject = {
					'status': 'fail',
					'message': 'Bearer token malformed.'
				}
				return make_response(jsonify(responseObject)), 401
		else:
			auth_token = ''
		if auth_token:
			resp = User.decode_auth_token(auth_token)
			if not isinstance(resp, str):
				user = User.query.filter_by(id=resp).first()
				responseObject = {
					'status': 'success',
					'data': {
						'user_id': user.id,
						'email': user.email,
						'admin': user.admin,
						'registered_on': user.registered_on
					}
				}
				return make_response(jsonify(responseObject)), 200
			responseObject = {
				'status': 'fail',
				'message': resp
			}
			return make_response(jsonify(responseObject)), 401
		else:
			responseObject = {
				'status': 'fail',
				'message': 'Provide a valid auth token.'
			}
			return make_response(jsonify(responseObject)), 401

#define API resource
registration_view = RegisterAPI.as_view( 'register_api' )
login_view = LoginAPI.as_view( 'login_api' )
logout_view = LogoutAPI.as_view( 'logout_api' )
user_view = UserAPI.as_view('user_api')

#add rules and API endpoints
auth_blueprint.add_url_rule(
	'/auth/register',
	view_func=registration_view,
	methods=[ 'POST' ]
)

auth_blueprint.add_url_rule(
	'/auth/login',
	view_func=login_view,
	methods=[ 'POST' ]
)

auth_blueprint.add_url_rule(
	'/auth/logout',
	view_func=logout_view,
	methods=[ 'POST' ]
)

auth_blueprint.add_url_rule(
	'/auth/status',
	view_func=user_view,
	methods=['GET']
)

#TODO: What did we change? Do the tests pass? What if the email is correct but the password is incorrect? What happens? Write a test for this!
