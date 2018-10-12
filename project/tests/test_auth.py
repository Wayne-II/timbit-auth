import unittest
import json

from project.server import db
from project.server.models import User
from project.tests.base import BaseTestCase

class TestAuthBlueprint( BaseTestCase ):
	def test_registration( self ):
		"""Test for user registration """
		with self.client:
			response = self.client.post(
				'/auth/register',
				data=json.dumps( dict (
					email='joe@gmail.com',
					password='123456'
				) ),
				content_type='application/json'
			)
			data = json.loads( response.data.decode() )
			self.assertTrue( data[ 'status' ] == 'success' )
			self.assertTrue( data[ 'message' ] == 'Successfully registered.' )
			self.assertTrue( data[ 'auth_token' ] )
			self.assertTrue( response.content_type == 'application/json' )
			self.assertEqual( response.status_code, 201 )

	def test_registered_with_existing_user( self ):
		"""Test registration with an email that's alreayd used"""
		user = User(
			email='joe@gmail.com',
			password='test'
		)
		db.session.add( user )
		db.session.commit()

		with self.client:
			response = self.client.post(
				'/auth/register',
				data=json.dumps( dict(
					email='joe@gmail.com',
					password='123456'
				) ),
				content_type='application/json'
			)
			data = json.loads( response.data.decode() )
			self.assertTrue( data[ 'status' ] == 'fail' )
			self.assertTrue(
				data[ 'message' ] == 'User not available'
			)
			self.assertTrue( response.content_type == 'application/json' )
			self.assertEqual( response.status_code, 202 )

		def test_registered_user_login(self):
			""" Test for login of registered user """
			with self.client:
				user = User(
					email='joe@gmail.com',
					password='123456'
				)
				db.session.add( user )
				db.session.commit()
				# registered user login
				response = self.client.post(
					'/auth/login',
					data=json.dumps(dict(
					email='joe@gmail.com',
					password='123456'
					)),
					content_type='application/json'
				)
				data = json.loads(response.data.decode())
				self.assertTrue(data['status'] == 'success')
				self.assertTrue(data['message'] == 'Successfully logged in.')
				self.assertTrue(data['auth_token'])
				self.assertTrue(response.content_type == 'application/json')
				self.assertEqual(response.status_code, 200)

	def test_non_registered_user_login(self):
		""" Test for login of non-registered user """
		with self.client:
			response = self.client.post(
				'/auth/login',
				data=json.dumps(dict(
				email='joe@gmail.com',
				password='123456'
				)),
				content_type='application/json'
			)
			data = json.loads(response.data.decode())
			print( 'data', data )
			self.assertTrue(data['status'] == 'fail')
			self.assertTrue(data['message'] == 'User does not exist.')
			self.assertTrue(response.content_type == 'application/json')
			self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
	unittest.main()
