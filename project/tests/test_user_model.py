<<<<<<< HEAD
# project/tests/test_user_model.py



=======
>>>>>>> jwt-auth
import unittest

from project.server import db
from project.server.models import User
from project.tests.base import BaseTestCase

<<<<<<< HEAD

class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

        self.assertTrue(User.decode_auth_token(
            auth_token.decode("utf-8") ) == 1)


if __name__ == '__main__':
    unittest.main()
=======
class TestUserModel( BaseTestCase ):
	def test_encode_auth_token( self ):
		user = User(
			email='test@test.com',
			password='test'
		)
		db.session.add( user )
		db.session.commit()
		auth_token = user.encode_auth_token( user.id )
		self.assertTrue( isinstance( auth_token, bytes ) )

	def test_decode_auth_token( self ):
		user = User(
			email='test@test.com',
			password='test'
		)
		db.session.add( user )
		db.session.commit()
		auth_token = user.encode_auth_token( user.id )
		self.assertTrue( isinstance( auth_token, bytes ) )
		self.assertTrue( User.decode_auth_token( auth_token ) == 1 )


if __name__ == '__main__':
	unittest.main()
>>>>>>> jwt-auth
