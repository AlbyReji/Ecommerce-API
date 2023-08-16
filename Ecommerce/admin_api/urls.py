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

    path('admin/order/list/',views.OrderListView.as_view(),name = "orderlist"),
    path('admin/order/list/<int:pk>/',views.OrderDetailView.as_view(),name = "order"),
    path('admin/order/update/<int:pk>/',views.OrderUpdateView.as_view(),name = "orderupdate"),

    path('admin/promotion-mail/',views.SendPromotionEmailView.as_view(),name = "orderlist"),



   
]