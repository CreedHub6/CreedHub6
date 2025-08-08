from django.contrib import admin
from .models import Restaurant, MenuItem, Order, Cart, OrderItem, CartItem, Review, Delivery, Profile

admin.site.register(Restaurant)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(OrderItem)
admin.site.register(CartItem)
admin.site.register(Review)
admin.site.register(Delivery)
admin.site.register(Profile)
