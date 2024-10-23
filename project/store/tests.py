from django.test import TestCase, Client
from django.contrib.auth import get_user_model

# Create your tests here.
class LoginTestCase(TestCase):
    def setup(self):
        pass
        
    
    def test_login_success(self):
        User = get_user_model()
        User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )
        c = Client()
        response = self.client.post('/accounts/login/', {
            'username':'testuser',
            'password':'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        r = c.login(username='testuser', password='testpassword')
        self.assertTrue(r)
        

    def test_login_empty_password(self):
        User = get_user_model()
        User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )
        c = Client()
        response = self.client.post('/accounts/login/', {
            'username':'testuser',
            'password':''
        })
        self.assertEqual(response.status_code, 200)
        r = c.login(username='testuser', password='')
        self.assertFalse(r)

        

    def test_login_failure(self):
        User = get_user_model()
        User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )
        c = Client()
        response = self.client.post('/accounts/login/', {
            'username':'testuser',
            'password':'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        r = c.login(username='testuser', password='wrongpassword')
        self.assertFalse(r)

    def test_empty(self):
        User = get_user_model()
        User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )
        c = Client()
        response = self.client.post('/accounts/login/', {
            
        })
        self.assertEqual(response.status_code, 200)
        r = c.login(username='', password='')
        self.assertFalse(r)

    def test_login_empty_username(self):
        User = get_user_model()
        User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )
        c = Client()
        response = self.client.post('/accounts/login/', {
            'password':'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        r = c.login(username='', password='testpassword')
        self.assertFalse(r)