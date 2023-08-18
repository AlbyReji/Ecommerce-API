from django.urls import path
from .import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name = "register"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('passwordreset/request/',views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('passwordreset/verify/',views.PasswordResetVerifyView.as_view(), name='password-reset-verify'),
    path('passwordreset/reset/',views.PasswordResetView.as_view(), name='password-reset'),

    path('user/adress/create/',views.AddressCreateview.as_view(), name='address create'),
    path('user/adress/detail/<int:pk>/',views.AddressDetailView.as_view(), name='address detail'),

    path('user/profile/create/',views.ProfileCreateview.as_view(), name='Profile create'),
    
    path('userproductlist/',views.UserProductlistview.as_view(),name = "userproductlist"),
    path('productdetail/<int:pk>/',views.UserProductView.as_view(),name = "productdetail"),


    path('addtocart/',views.AddToCartView.as_view(), name='add-to-cart'),
    path('viewcart/', views.CartListView.as_view(), name='viewcart'),
    path('cartupdate/<int:pk>/', views.CartUpdateView.as_view(), name='cartupdate'),
    path('cartdelete/<int:pk>/', views.CartDeleteView.as_view(), name='cartdelete'),

    path('order/',views.OrderView.as_view(), name='order'),
    path('orderlist/',views.OrderListView.as_view(), name='orderlist'),






]