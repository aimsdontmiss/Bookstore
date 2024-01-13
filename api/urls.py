from django.urls import path, include;
from django.conf import settings;
from django.conf.urls.static import static;
from .views import *;
from rest_framework_simplejwt.views import ( 
    TokenRefreshView, TokenVerifyView 
    );




urlpatterns = [

    path('', apiOverview, name='api-overview'),


    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('user-list/', userList, name='user-list'),
    path('user-register/', userRegister, name='user-register'),

    path('product-list/', productList, name='product-list'),
    path('product-detail/<str:pk>/', productDetail, name='product-detail'),
    path('product-create/', productCreate, name='product-create'),
    path('product-update/<str:pk>/', productUpdate, name='product-update'),
    path('product-delete/<str:pk>/', productDelete, name='product-delete'),

    path('order-list/', orderList, name='order-list'),
    path('order-detail/<str:customer_id>/', orderDetail, name='order-detail'),
    path('order-create/', orderCreate, name='order-create'),
    path('order-update/<str:pk>/', orderUpdate, name='order-update'),
    path('order-delete/<str:pk>/', orderDelete, name='order-delete'),

    path('order-item-list/<int:order_id>/', orderItemList, name='order-list'),
    path('order-item-detail/<int:order_id>/<int:product_id>/', orderItemDetail, name='order-detail'),
    path('order-item-create/', orderItemCreate, name='order-create'),
    path('order-item-update/<int:pk>/', orderItemUpdate, name='order-update'),
    path('order-item-delete/<str:pk>/', orderItemDelete, name='order-delete'),

    path('customer-list/', customerList, name='customer-list'),
    path('customer-detail/<str:user_id>/', customerDetail, name='customer-detail'),
    path('customer-create/', customerCreate, name='customer-create'),
    path('customer-update/<str:pk>/', customerUpdate, name='customer-update'),
    path('customer-delete/<str:pk>/', customerDelete, name='customer-delete'),

    # path('shipping-address-list/', shippingAddressList, name='shipping-address-list'),
    # path('shipping-address-detail/<str:customer_id>/', shippingAddressDetail, name='shipping-address-detail'),
    # path('shipping-address-create/', shippingAddressCreate, name='shipping-address-create'),
    # path('shipping-address-update/<str:pk>/', shippingAddressUpdate, name='shipping-address-update'),
    # path('shipping-address-delete/<str:pk>/', shippingAddressDelete, name='shipping-address-delete'),

    path('purchase-list/', purchaseList, name='purchase-list'),
    path('purchase-detail/<str:customer_id>/', purchaseDetail, name='purchase-detail'),
    path('purchase-create/', purchaseCreate, name='purchase-create'),
    path('purchase-update/<str:pk>/', purchaseUpdate, name='purchase-update'),
    path('purchase-delete/<str:pk>/', purchaseDelete, name='purchase-delete'),

    path('create-checkout-session/<int:order_id>/', stripeCheckout, name='create-checkout-session'),
    path('stripe-webhook/', webhook_view, name='stripe-webhook'),
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token')
    # path('stripe-checkout-session/', stripe_checkout, name='checkout-session'),


    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)