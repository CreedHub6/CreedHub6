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
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
