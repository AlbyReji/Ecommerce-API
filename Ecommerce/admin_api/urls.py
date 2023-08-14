from django.urls import path
from .import views


urlpatterns = [
    path('categorycreate/',views.CategoryCreateView.as_view(),name = "categorycreate"),
    path('categorylist/',views.CategoryListView.as_view(),name = "categorylist"),
    path('categorydetail/<int:pk>/',views.CategoryDetailView.as_view(),name = "categorydetail"),

    path('productcreate/',views.ProductCreateView.as_view(),name = "productcreate"),
    path('productlist/',views.ProductListView.as_view(),name = "productlist"),
    path('productdetail/<int:pk>/',views.ProductDetailView.as_view(),name = "productdetail"),

    path('userlist/',views.UserListView.as_view(),name = "userlist"),
    path('userdelete/<int:pk>/',views.UserDeleteView.as_view(),name = "userdelete"),
   
]