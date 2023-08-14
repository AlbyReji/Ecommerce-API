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

    path('userproductlist/',views.UserProductlistview.as_view(),name = "userproductlist"),
    path('productdetail/<int:pk>/',views.UserProductView.as_view(),name = "productdetail"),


    path('addtocart/',views.AddToCartView.as_view(), name='add-to-cart'),
    path('viewcart/', views.CartListView.as_view(), name='viewcart'),


]