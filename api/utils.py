import stripe
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.response import Response



def stripe_checkout(product_name="test product", product_price=1000):
    
        stripe_product_obj = stripe.Product.create(name=product_name)   
        stripe_product_id = stripe_product_obj.id
        stripe_price_obj = stripe.Price.create(
            unit_amount=product_price,
            currency='cad',
            product=stripe_product_id,
        )
        stripe_price_id = stripe_price_obj.id
    
        line_item = {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': product_name,
                },
                'unit_amount': product_price,
            },
            'quantity': 1,
        }

    
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=line_item,
                payment_method_types=['card'],
                mode='payment',
                success_url= settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url= settings.SITE_URL + '/?cancelled=true',
            )
            
            print(checkout_session.url)
    