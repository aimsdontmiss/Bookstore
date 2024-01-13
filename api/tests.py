from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import *
import responses

# class StripeCheckoutTestCase(TestCase):
#     def test_stripe_checkout_success(self):
#         # Your test code for successful payment scenario
#         response = self.client.post(reverse('stripe_checkout', args=[your_order_id]), data={})
#         self.assertEqual(response.status_code, 303)  # Check for the correct redirect status code


#     def test_stripe_checkout_failure(self):
#         # Your test code for payment failure scenario
#         response = self.client.post(reverse('stripe_checkout', args=[your_order_id]), data={})
#         self.assertEqual(response.status_code, 500) 

class StripeCheckoutTestCase(TestCase):
    @responses.activate
    def test_stripe_checkout_success(self):
        # Mock the Stripe API response for successful checkout
        responses.add(responses.POST, 'https://api.stripe.com/v1/checkout/sessions', status=200, json={})
        
        # Your test code
        response = self.client.post(reverse('stripe_checkout', args=[your_order_id]), data={})
        self.assertEqual(response.status_code, 303)

    @responses.activate
    def test_stripe_checkout_failure(self):
        # Mock the Stripe API response for failed checkout
        responses.add(responses.POST, 'https://api.stripe.com/v1/checkout/sessions', status=500, json={})
        
        # Your test code
        response = self.client.post(reverse('stripe_checkout', args=[your_order_id]), data={})
        self.assertEqual(response.status_code, 500) 
