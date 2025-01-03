from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('menu/<int:restaurant_id>/', views.menu, name='menu'),
    path('order/', views.place_order, name='place_order'),
    path('order-history/', views.order_history, name='order_history'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('signup/', views.signup, name='user_signup'),

    path('view_cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:menu_item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
