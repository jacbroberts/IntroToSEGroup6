from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from .models import Product, CartItem, SoldItems
from accounts.models import Customer
from .forms import PaymentForm
from django.urls import reverse
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
            'user_type':'user_type',
            'username':'testuser',
            'password':'testpassword'
        })
        self.assertEqual(response.status_code, 200)
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
            'user_type':'user_type',
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
            'user_type':'user_type',
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

class PaymentFormTests(TestCase):

    def setUp(self):
        # Valid data to reuse in tests
        self.valid_data = {
            'card_number': '1234567812345678',
            'expiry_date': '12/25',
            'cvv': '123',
            'billing_address': '123 Main St',
            'billing_city': 'New York',
            'billing_state': 'NY',
            'billing_zip': '10001',
            'different_shipping': False,
        }

    def test_valid_payment_info(self):
        """Test that valid payment info is processed successfully."""
        User = get_user_model()
        user = User.objects.create_user(username='testuser1', password='testpassword')
        client = Client()
        self.client.force_login(user) # Force the user to be logged in
        response = self.client.post(reverse('store:validate_payment'), data=self.valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Payment processed successfully.")

    def test_invalid_card_number(self):
        """Test that an invalid card number (not 16 digits) is rejected."""
        User = get_user_model()
        user = User.objects.create_user(username='testuser2', password='testpassword')
        client = Client()
        self.client.force_login(user) # Force the user to be logged in
        invalid_data = self.valid_data.copy()
        invalid_data['card_number'] = '1234'  # Invalid card number
        response = self.client.post(reverse('store:validate_payment'), data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "card_number")  # Should contain error for card_number

    def test_invalid_cvv(self):
        """Test that an invalid CVV (not 3 digits) is rejected."""
        User = get_user_model()
        user = User.objects.create_user(username='testuser3', password='testpassword')
        client = Client()
        self.client.force_login(user) # Force the user to be logged in
        invalid_data = self.valid_data.copy()
        invalid_data['cvv'] = '12'  # Invalid CVV
        response = self.client.post(reverse('store:validate_payment'), data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cvv")  # Should contain error for cvv

    def test_invalid_expiry_date(self):
        """Test that an invalid expiry date is rejected."""
        User = get_user_model()
        user = User.objects.create_user(username='testuser4', password='testpassword')
        client = Client()
        self.client.force_login(user) # Force the user to be logged in
        invalid_data = self.valid_data.copy()
        invalid_data['expiry_date'] = '13/25'  # Invalid expiry date
        response = self.client.post(reverse('store:validate_payment'), data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "expiry_date")  # Should contain error for expiry_date

    def test_missing_billing_address(self):
        """Test that a missing billing address is rejected."""
        User = get_user_model()
        user = User.objects.create_user(username='testuser5', password='testpassword')
        client = Client()
        client.force_login(user)  # Force the user to be logged in
        
        # Define valid data initially, then remove the billing address
        invalid_data = self.valid_data.copy()  
        invalid_data['billing_address'] = ''  # Missing billing address
        
        response = client.post(reverse('store:validate_payment'), data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "billing_address")  # Should contain error for billing_address



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
        
    def test_add_product_success(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client = Client()
        self.client.force_login(user) # Force the user to be logged in

        response = self.client.post('/store/add_product', {
            'name':'testname',
            'price':'30',
            'remaining_quantity':'10',
            'description':'testdescription'
        })
        self.assertEqual(response.status_code, 301)
    
    def test_add_product_price_2high(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client = Client()
        self.client.force_login(user) # Force the user to be logged in

        response = self.client.post('/store/add_product', {
            'name':'testname',
            'price':'101',
            'remaining_quantity':'10',
            'description':'testdescription'
        })
        self.assertEqual(response.status_code, 301)
    
    def test_add_product_quantity_2high(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client = Client()
        self.client.force_login(user) # Force the user to be logged in

        response = self.client.post('/store/add_product', {
            'name':'testname',
            'price':'30',
            'remaining_quantity':'60',
            'description':'testdescription'
        })
        self.assertEqual(response.status_code, 301)

    def test_add_product_success_despite_noDesc(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client = Client()
        self.client.force_login(user) # Force the user to be logged in

        response = self.client.post('/store/add_product', {
            'name':'testname',
            'price':'30',
            'remaining_quantity':'10',
            'description':''
        })
        self.assertEqual(response.status_code, 301)
    
    def test_add_product_no_name(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client = Client()
        self.client.force_login(user) # Force the user to be logged in

        response = self.client.post('/store/add_product', {
            'name':'',
            'price':'30',
            'remaining_quantity':'10',
            'description':'testdescription'
        })
        self.assertEqual(response.status_code, 301)
        
