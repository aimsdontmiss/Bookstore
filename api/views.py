# from django.shortcuts import get_object_or_404;
import stripe;
from django.conf import settings;
from django.db import IntegrityError;
from django.shortcuts import render, redirect;
from django.contrib.auth.models import User
from rest_framework.decorators import api_view;
from rest_framework.response import Response;
from rest_framework import status;
from rest_framework.views import APIView;
from django.db import transaction;
from django.middleware.csrf import get_token;
from django.views.decorators.csrf import csrf_exempt;
# from '../litdot/.env' import SIGNING_SECRET;

from .serializers import *;
from .models import *;
from djstripe import webhooks;
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer;
from rest_framework_simplejwt.views import TokenObtainPairView;


# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY;



@api_view(['GET'])
def apiOverview(request):
    api_urls = {

        'User List': 'user-list/',   
        'User Register': 'user-register/',
        
        'Token Obtain Pair': 'token/',
        'Token Refresh': 'token/refresh/',
        'Token Verify': 'token/verify/',

        'Stripe Checkout': 'create-checkout-session/',

        'Product List': 'product-list/',
        'Product Detail': 'product-detail/',
        'Product Create': 'product-create/',
        'Product Update': 'product-update/',
        'Product Delete': 'product-delete/',

        'Order List': 'order-list/',
        'Order Detail': 'order-detail/',
        'Order Create': 'order-create/',
        'Order Update': 'order-update/',
        'Order Delete': 'order-delete/',

        'Customer List': 'customer-list/',
        'Customer Detail': 'customer-detail/',
        'Customer Create': 'customer-create/',
        'Customer Update': 'customer-update/',
        'Customer Delete': 'customer-delete/',

        'Order Item List': 'order-item-list/',
        'Order Item Detail': 'order-item-detail/',
        'Order Item Create': 'order-item-create/',
        'Order Item Update': 'order-item-update/',
        'Order Item Delete': 'order-item-delete/',

        'Purchase List': 'purchase-list/',
        'Purchase Detail': 'purchase-detail/',
        'Purchase Create': 'purchase-create/',
        'Purchase Update': 'purchase-update/',
        'Purchase Delete': 'purchase-delete/',


    }
    return Response(api_urls)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


'''
                !-----------> USER VIEWS <-----------!
'''


@api_view(['GET'])
def userList(request):

    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def userRegister(request):
    
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.create(serializer.validated_data)

    return Response(serializer.data) 


'''
                !-----------> PRODUCT VIEWS <-----------!
'''

@api_view(['GET'])
def productList(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def productDetail(request, pk):
    products = Product.objects.get(id=pk)
    serializer = ProductSerializer(products, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def productCreate(request):
    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['PUT'])
def productUpdate(request, pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(instance=product, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def productDelete(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return Response("Item was successfully deleted")


'''
                !-----------> ORDER VIEWS <-----------!
'''

@api_view(['GET'])
def orderList(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def orderDetail(request, customer_id):
    try:
        # Try to get the existing order
        order = Order.objects.get(customer__id=customer_id)
        serializer = OrderSerializer(order, many=False)

    except Order.DoesNotExist:
        try:
            # If the order doesn't exist, create a new one
            order = Order.objects.create(customer_id=customer_id)
            serializer = OrderSerializer(order, many=False)
            if serializer.is_valid():
                serializer.save()

        except IntegrityError:
            # Handle the case where another thread or process created the order concurrently
            order = Order.objects.get(customer__id=customer_id)
            serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def orderCreate(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['PUT'])
def orderUpdate(request, pk):
    order = Order.objects.get(id=pk)
    serializer = OrderSerializer(instance=order, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def orderDelete(request, pk):
    order = Order.objects.get(id=pk)
    order.delete()
    return Response("Order was successfully deleted")

'''
                !-----------> ORDER ITEM VIEWS <-----------!
'''

@api_view(['GET'])
def orderItemList(request, order_id):
    orderItem = OrderItem.objects.filter(order__id=order_id)
    serializer = OrderItemSerializer(orderItem, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def orderItemDetail(request, order_id, product_id):
    orderItem = OrderItem.objects.get(order__id=order_id, product__id=product_id)
    serializer = OrderItemSerializer(orderItem, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def orderItemCreate(request):
    serializer = OrderItemSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
def orderItemUpdate(request, pk):
    orderItem = OrderItem.objects.get(id=pk)
    serializer = OrderItemSerializer(instance=orderItem, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def orderItemDelete(request, pk):
    orderItem = OrderItem.objects.get(id=pk)
    orderItem.delete()
    return Response("Order Item was successfully deleted")


'''
                !-----------> CUSTOMER VIEWS <-----------!
'''


@api_view(['GET'])
def customerList(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def customerDetail(request, user_id):
    customers = Customer.objects.get(user__id=user_id)
    serializer = CustomerSerializer(customers, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def customerCreate(request):
    serializer = CustomerSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['PUT'])
def customerUpdate(request, pk):
    customer = Customer.objects.get(id=pk)
    serializer = CustomerSerializer(instance=customer, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def customerDelete(request, pk):
    customer = Customer.objects.get(id=pk)
    customer.delete()
    return Response("customer was successfully deleted")


'''
                !-----------> PURCHASE VIEWS <-----------!
'''


@api_view(['GET'])
def purchaseList(request):
    purchases = Purchase.objects.all()
    serializer = PurchaseSerializer(purchases, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def purchaseDetail(request, user_id):
    purchase = Purchase.objects.get(user__id=user_id)
    serializer = PurchaseSerializer(purchase, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def purchaseCreate(request):
    serializer = PurchaseSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['PUT'])
def purchaseUpdate(request, pk):
    purchase = Purchase.objects.get(id=pk)
    serializer = PurchaseSerializer(instance=purchase, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def purchaseDelete(request, pk):
    purchase = Purchase.objects.get(id=pk)
    purchase.delete()
    return Response("purchase was successfully deleted")



'''
                !-----------> STRIPE VIEWS <-----------!
'''


@api_view(['POST'])
@transaction.atomic
def stripeCheckout(request, order_id):
    
    lines = []
    order = Order.objects.get(id=order_id)
    order_item_list = OrderItem.objects.filter(order__id=order_id)


    for order_item in order_item_list:
        with transaction.atomic():
            product_id = order_item.product.id
            product = Product.objects.select_for_update().get(id=product_id)
            product.inv -= order_item.quantity
            product.save()

        # Stripe API call to create a product
        stripe_product_obj = stripe.Product.create(name=product.title)   
        stripe_product_id = stripe_product_obj.id

        # Stripe API call to create a price
        stripe_price_obj = stripe.Price.create(
            unit_amount=int(product.price * 100),
            currency='usd',
            product=stripe_product_id,
        )
        stripe_price_id = stripe_price_obj.id

        # Stripe API call to create a customer
        stripe_customer_obj = stripe.Customer.create(
            email=order.customer.email,
            name=order.customer.name
        )

        # Create a line item for the order           
        line_item = {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': product.title,
                },
                'unit_amount': int(product.price * 100),
            },
            'quantity': order_item.quantity,
        }
        lines.append(line_item)


    if not lines:
        return Response({'error': 'No line items in the order.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        checkout_session = stripe.checkout.Session.create(
            customer=stripe_customer_obj.id,
            shipping_address_collection={
                'allowed_countries': ['US', 'CA']
            },
            line_items=lines,
            payment_method_types=['card'],
            mode='payment',
            # success_url= settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
            success_url= settings.SITE_URL + '/my-order/success/?success=true&session_id={CHECKOUT_SESSION_ID}',

            cancel_url= settings.SITE_URL + '/?cancelled=true',
        )
        return redirect(checkout_session.url)

    except stripe.error.StripeError as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def webhook_view(request):
    payload = request.body
    sig_header = request.headers['Stripe-Signature']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_SIGNING_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return Response({'error': str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return Response({'error': str(e)}, status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object'] # contains a stripe.PaymentIntent

        payment_intent_id = payment_intent['id']
        customer = payment_intent['shipping']['name']
        shipping_address_data = payment_intent['shipping']['address']

        charge_id = payment_intent_id[3:]
        print(charge_id)

        order = Order.objects.get(customer__name=customer)
        order.complete = True
        order.transaction_id = charge_id
        order.save()
        customer_id = Customer.objects.get(name=customer)
        print(customer_id, order, shipping_address_data)


        # Use the shipping data to create fields for shipping address model
        city = shipping_address_data['city']
        state = shipping_address_data['state']
        country = shipping_address_data['country']
        postal_code = shipping_address_data['postal_code']
        address = shipping_address_data['line1']

        # Consolidate the address data into a single string
        if not shipping_address_data['line2']:
            address = shipping_address_data['line1']
            print(address)
        else:
            address = shipping_address_data['line1'] + ', ' + shipping_address_data['line2']
            print(address)

        # Create a shipping address object
        shipping_address, created = ShippingAddress.objects.get_or_create(
            customer=customer_id,
            order=order,
            address=address,
            city=city,
            province=state,
            country=country,
            postcode=postal_code
        )
        shipping_address.save();

        # Check if the shipping address was saved
        if shipping_address:
            print('Shipping Address Saved')
        else:
            print('Shipping Address Not Saved')


        # Create a Purchase model object
        orderitems = OrderItem.objects.filter(order__id=order.id)
        purchase_item = [{'product': item.product.title, 'quantity': item.quantity, 
                        'price': str(item.product.price) } for item in orderitems]  
        
        purchase = Purchase.objects.create(
                customer=customer_id,
                order=order,
                purchase_items=purchase_item,
                charge_id=charge_id,
                shipping_address=shipping_address
            )
        purchase.save();
        print(purchase, purchase_item)


    return Response(status=200)


'''
                !-----------> CSRF VIEW <-----------!
'''

def get_csrf_token(request):
    csrf_token = get_token(request)
    return Response({'csrfToken': csrf_token})

