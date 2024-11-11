from django.test import TestCase, Client
from django.contrib.auth import get_user_model

# Create your tests here.
class RegistrationTestCase(TestCase):
    def setup(self):
        pass
        
    
    def test_registration_success(self):
        User = get_user_model()
        response = self.client.post('/accounts/signup/', {
            'username':'testuser',
            'user_type':'Customer',
            'password1':'testpassword',
            'password2':'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        
        

    def test_registration_nonunique_user(self):
        User = get_user_model()
        response = self.client.post('/accounts/signup/', {
            'username':'testuser',
            'user_type':'Customer',
            'password1':'testpassword',
            'password2':'testpassword'
        })
        response = self.client.post('/accounts/signup/', {
            'username':'testuser',
            'user_type':'Customer',
            'password1':'testpassword',
            'password2':'testpassword'
        })
        self.assertEqual(response.status_code, 200)

        

    def test_registration_shortpassword(self):
        response = self.client.post('/accounts/signup/', {
            'username':'testuser',
            'user_type':'Customer',
            'password1':'test',
            'password2':'test'
        })
        self.assertEqual(response.status_code, 200)

    def test_customer(self):
        response = self.client.post('/accounts/signup/', {
                'username':'testuser',
                'user_type':'Customer',
                'password1':'testpassword',
                'password2':'testpassword'
            })
        response = self.client.post('/accounts/make_customer/')
        response = self.client.post('/accounts/edit_customer/', {
            "street_address_1":"test street",
            "street_address_2":"test apt",
            "city":"city",
            "state":"MS",
            "zip":"12345"
        })
        self.assertEqual(response.status_code, 302)

    def test_seller(self):
        response = self.client.post('/accounts/signup/', {
                'username':'testuser',
                'user_type':'Customer',
                'password1':'testpassword',
                'password2':'testpassword'
            })
        response = self.client.post('/accounts/make_seller/')
        response = self.client.post('/accounts/edit_seller/', {
            "business_name":"test Business"
        })
        self.assertEqual(response.status_code, 302)