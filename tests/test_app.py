import unittest
from flask import Flask
from ..website import create_app, db  # Import your Flask app factory function
from ..website.models import User  # Import User model from models.py
from werkzeug.security import generate_password_hash

class BankAppTests(unittest.TestCase):
    
    def setUp(self):
        """Set up test client and database."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for tests
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            self.create_test_user()
    
    def tearDown(self):
        """Clean up database after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def create_test_user(self):
        """Create a test user for login purposes."""
        user = User(
            username='testuser', 
            mobile='1234567890',
            password=generate_password_hash('password123', method='pbkdf2:sha256'),
            pin=generate_password_hash('1234', method='pbkdf2:sha256'),
            age=25,
            gender='Male',
            account='Savings',
            balance=1000.0
        )
        db.session.add(user)
        db.session.commit()
    
    def test_register(self):
        """Test user registration."""
        response = self.client.post('/register', data={
            'username': 'newuser',
            'mobile': '0987654321',
            'password': 'password123',
            'pin': '1234',
            'age': '30',
            'gender': 'Female',
            'account': 'Current'
        }, follow_redirects=True)
  
    
    def test_login(self):
        """Test user login."""
        response = self.client.post('/', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)

    
    def test_invalid_login(self):
        """Test login with incorrect credentials."""
        response = self.client.post('/', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        }, follow_redirects=True)

    
    def test_deposit(self):
        """Test deposit functionality."""
        self.client.post('/', data={'username': 'testuser', 'password': 'password123'}, follow_redirects=True)
        response = self.client.post('/deposit', data={'deposit': '500', 'pin': '1234'}, follow_redirects=True)
    
    
    def test_withdraw(self):
        """Test withdraw functionality."""
        self.client.post('/', data={'username': 'testuser', 'password': 'password123'}, follow_redirects=True)
        response = self.client.post('/withdraw', data={'withdraw': '200', 'pin': '1234'}, follow_redirects=True)
    
    def test_insufficient_balance_withdraw(self):
        """Test withdrawing more than the available balance."""
        self.client.post('/', data={'username': 'testuser', 'password': 'password123'}, follow_redirects=True)
        response = self.client.post('/withdraw', data={'withdraw': '5000', 'pin': '1234'}, follow_redirects=True)
    

if __name__ == '__main__':
    unittest.main()
