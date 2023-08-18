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

    path('user/passwordreset/request/',views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('user/passwordreset/verify/',views.PasswordResetVerifyView.as_view(), name='password_reset_verify'),
    path('user/passwordreset/reset/',views.PasswordResetView.as_view(), name='password_reset'),

    path('user/adress/create/',views.AddressCreateview.as_view(), name='address_create'),
    path('user/adress/detail/<int:pk>/',views.AddressDetailView.as_view(), name='address_detail'),

    path('user/profile/create/',views.ProfileCreateview.as_view(), name='Profile_create'),

    path('user/category/list/',views.CatgorylistView.as_view(),name = "category_list"),
    path('user/product/list/',views.UserProductlistview.as_view(),name = "user_product_list"),
    path('user/product/detail/<int:pk>/',views.UserProductView.as_view(),name = "product_detail"),


    path('user/addtocart/',views.AddToCartView.as_view(), name='add_to_cart'),
    path('user/view/cart/', views.CartListView.as_view(), name='view_cart'),
    path('user/cart/update/<int:pk>/', views.CartUpdateView.as_view(), name='cart_update'),
    path('user/cart/delete/<int:pk>/', views.CartDeleteView.as_view(), name='cart_delete'),

    path('user/order/',views.OrderView.as_view(), name='order'),
    path('user/order/list/',views.OrderListView.as_view(), name='orderlist'),

    path('nonuser/category/list/',views.NonUserCatgorylistView.as_view(),name = "Nonuser_category_list"),
    path('nonuser/product/list/',views.NonUserProductlistview.as_view(),name = "Nonuser_product_list"),
    path('nonuser/product/detail/<int:pk>/',views.NonUserProductView.as_view(),name = "Nonuser_product_detail"),

]