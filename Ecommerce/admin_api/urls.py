from django.urls import path
from .import views


urlpatterns = [
    path('admin/category/create/',views.CategoryCreateView.as_view(),name = "categorycreate"),
    path('admin/category/list/',views.CategoryListView.as_view(),name = "categorylist"),
    path('admin/category/detail/<int:pk>/',views.CategoryDetailView.as_view(),name = "categorydetail"),

    path('admin/product/create/',views.ProductCreateView.as_view(),name = "productcreate"),
    path('admin/product/list/',views.ProductListView.as_view(),name = "productlist"),
    path('admin/product/detail/<int:pk>/',views.ProductDetailView.as_view(),name = "productdetail"),

    path('admin/user/list/',views.UserListView.as_view(),name = "userlist"),
    path('admin/user/delete/<int:pk>/',views.UserDeleteView.as_view(),name = "userdelete"),

    path('admin/order/list/',views.OrderListView.as_view(),name = "orderlist"),
    path('admin/order/list/<int:pk>/',views.OrderDetailView.as_view(),name = "order"),
    path('admin/order/update/<int:pk>/',views.OrderUpdateView.as_view(),name = "orderupdate"),

    path('admin/promotion/mail/',views.SendPromotionEmailView.as_view(),name = "orderlist"),

]