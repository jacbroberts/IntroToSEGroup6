from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Product, CartItem, SoldItems
from accounts.models import Customer
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


    def test_sell(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client = Client()
        self.client.force_login(user) # Force the user to be logged in

        product = Product.objects.create(seller=user,name="iPhone",price=100.00,remaining_quantity=10,description="newest iphone for sale")
        customer = Customer.objects.create(user=user,street_address_1="1",street_address_2="1",city="starkville",state="MS",zip_code=12345)

        response = self.client.get('/store/products/')
        self.assertEqual(response.status_code, 200)

        cartItem = CartItem.objects.create(user=user,product=product,quantity=1)

        response = self.client.get("/store/cart/")

        self.assertContains(response, "iPhone")

        response = self.client.post('/store/process_payment/', {
            "card_number":"1",
            "expiry_date":"1",
            "cvv":"1",
            "billing_address":"1",
            "billing_city":"1",
            "billing_state":"1",
            "billing_zip":"1",
            "shipping_address":"",
            "shipping_city":"",
            "shipping_state":"",
            "shipping_zip":""

        })

        self.assertContains(response, "Payment processed successfully.")
        
        response = self.client.get("/store/sold/")

        self.assertEqual(response.status_code,200)

        self.assertContains(response, "iPhone")

    def test_sell_no_buyer(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client = Client()
        self.client.force_login(user) # Force the user to be logged in

        product = Product.objects.create(seller=user,name="iPhone",price=100.00,remaining_quantity=10,description="newest iphone for sale")
        customer = Customer.objects.create(user=user,street_address_1="1",street_address_2="1",city="starkville",state="MS",zip_code=12345)

        response = self.client.get('/store/products/')
        self.assertEqual(response.status_code, 200)

        cartItem = CartItem.objects.create(user=user,product=product,quantity=1)

        response = self.client.get("/store/cart/")

        self.assertContains(response, "iPhone")

        
        
        response = self.client.get("/store/sold/")

        self.assertEqual(response.status_code,200)

        self.assertNotContains(response, "iPhone")

    def test_sell_payment_info(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client = Client()
        self.client.force_login(user) # Force the user to be logged in

        product = Product.objects.create(seller=user,name="iPhone",price=100.00,remaining_quantity=10,description="newest iphone for sale")
        customer = Customer.objects.create(user=user,street_address_1="1",street_address_2="1",city="starkville",state="MS",zip_code=12345)

        response = self.client.get('/store/products/')
        self.assertEqual(response.status_code, 200)

        cartItem = CartItem.objects.create(user=user,product=product,quantity=1)

        response = self.client.get("/store/cart/")

        self.assertContains(response, "iPhone")

        response = self.client.post('/store/process_payment/', {
            "card_number":"1234123412341234",
            "expiry_date":"05/25",
            "cvv":"123",
            "billing_address":"1",
            "billing_city":"1",
            "billing_state":"1",
            "billing_zip":"1",
            "shipping_address":"",
            "shipping_city":"",
            "shipping_state":"",
            "shipping_zip":""

        })

        self.assertContains(response, "Payment processed successfully.")
        
        response = self.client.get("/store/sold/")

        self.assertEqual(response.status_code,200)

        self.assertContains(response, "1234123412341234")
        self.assertContains(response, "05/25")
        self.assertContains(response, "123")

    def test_sell_payment_quantity(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client = Client()
        self.client.force_login(user) # Force the user to be logged in

        product = Product.objects.create(seller=user,name="iPhone",price=100.00,remaining_quantity=10,description="newest iphone for sale")
        customer = Customer.objects.create(user=user,street_address_1="1",street_address_2="1",city="starkville",state="MS",zip_code=12345)

        response = self.client.get('/store/products/')
        self.assertEqual(response.status_code, 200)

        cartItem = CartItem.objects.create(user=user,product=product,quantity=2)

        response = self.client.get("/store/cart/")

        self.assertContains(response, "iPhone")

        response = self.client.post('/store/process_payment/', {
            "card_number":"1234123412341234",
            "expiry_date":"05/25",
            "cvv":"123",
            "billing_address":"1",
            "billing_city":"1",
            "billing_state":"1",
            "billing_zip":"1",
            "shipping_address":"",
            "shipping_city":"",
            "shipping_state":"",
            "shipping_zip":""

        })

        self.assertContains(response, "Payment processed successfully.")
        
        response = self.client.get("/store/sold/")

        self.assertEqual(response.status_code,200)

        self.assertContains(response, "testuser bought 2 iPhone")

    def test_sell_shipped_product(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client = Client()
        self.client.force_login(user) # Force the user to be logged in

        product = Product.objects.create(seller=user,name="iPhone",price=100.00,remaining_quantity=10,description="newest iphone for sale")
        customer = Customer.objects.create(user=user,street_address_1="1",street_address_2="1",city="starkville",state="MS",zip_code=12345)

        response = self.client.get('/store/products/')
        self.assertEqual(response.status_code, 200)

        cartItem = CartItem.objects.create(user=user,product=product,quantity=2)

        response = self.client.get("/store/cart/")

        self.assertContains(response, "iPhone")

        response = self.client.post('/store/process_payment/', {
            "card_number":"1234123412341234",
            "expiry_date":"05/25",
            "cvv":"123",
            "billing_address":"1",
            "billing_city":"1",
            "billing_state":"1",
            "billing_zip":"1",
            "shipping_address":"",
            "shipping_city":"",
            "shipping_state":"",
            "shipping_zip":""

        })

        self.assertContains(response, "Payment processed successfully.")
        
        response = self.client.get("/store/sold/")

        self.assertEqual(response.status_code,200)

        self.assertContains(response, "testuser bought 2 iPhone")

        id = SoldItems.objects.get(user=user)
        id = id.id

        response = self.client.get(f"/store/sold/{id}")
        