from django.contrib import admin
from user_api.models import (User,
                    Address,
                    UserProfile,
                    CartItem,
                    Order,
                    OrderItem)


admin.site.register(User)
admin.site.register(Address)
admin.site.register(UserProfile)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)


