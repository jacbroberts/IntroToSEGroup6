from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Product

# Create your tests here.
class StoreTestCase(TestCase):
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

    def test_search_none(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client = Client()
        self.client.force_login(user) # Force the user to be logged in

        #should return all products
        response = self.client.get('/store/products/')
        self.assertEqual(response.status_code, 200)

    def test_search_in(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client = Client()
        self.client.force_login(user) # Force the user to be logged in

        product = Product.objects.create(name="iPhone",price=100.00,remaining_quantity=10,description="newest iphone for sale")

        response = self.client.get('/store/products/?search=iphone')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "iPhone")

    def test_search_out(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client = Client()
        self.client.force_login(user) # Force the user to be logged in

        product = Product.objects.create(name="iPhone",price=100.00,remaining_quantity=10,description="newest iphone for sale")
        product = Product.objects.create(name="Samsung Galaxy 10",price=100.00,remaining_quantity=10,description="newest samsung for sale")

        response = self.client.get('/store/products/?search=iphone')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Samsung")

    def test_user_logged_out(self):
        product = Product.objects.create(name="iPhone",price=100.00,remaining_quantity=10,description="newest iphone for sale")
        product = Product.objects.create(name="Samsung Galaxy 10",price=100.00,remaining_quantity=10,description="newest samsung for sale")

        response = self.client.get('/store/products/?search=iphone')
        self.assertEqual(response.status_code, 302)

    def test_all_products(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client = Client()
        self.client.force_login(user) # Force the user to be logged in

        product = Product.objects.create(name="iPhone",price=100.00,remaining_quantity=10,description="newest iphone for sale")
        product = Product.objects.create(name="Samsung Galaxy 10",price=100.00,remaining_quantity=10,description="newest samsung for sale")

        response = self.client.get('/store/products/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Samsung")
        self.assertContains(response, "iPhone")



