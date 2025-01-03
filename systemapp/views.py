from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, MenuItem, Order,OrderItem,Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal

def home(request):
    return render(request, 'systemapp/home.html')

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'systemapp/restaurant_list.html', {'restaurants': restaurants})

def menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = restaurant.menuitem_set.all()
    return render(request, 'systemapp/menu.html', {'restaurant': restaurant, 'menu_items': menu_items})

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem

@login_required
def view_cart(request):
    # Get the user's cart (if exists)
    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        # If there's no cart, we could either create one or show an empty message
        return render(request, 'systemapp/view_cart.html', {'cart_items': [], 'total_price': 0})

    # Get the cart items for the user's cart
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate the total price of items in the cart
    total_price = sum(item.menu_item.price * item.quantity for item in cart_items)

    # Return the cart and total price to the template
    return render(request, 'systemapp/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, menu_item_id):
    # Get the menu item that the user wants to add to the cart
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)

    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get or create the CartItem, if it already exists, update the quantity
    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)

    # If the item already exists in the cart, increment its quantity
    if not created:
        cart_item.quantity += 1
    cart_item.save()  # Save the cart item to the database

    return redirect('view_cart')  # Redirect to the view cart page

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('view_cart')

# Order Views
@login_required
def place_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items:
        return JsonResponse({'error': 'Your cart is empty'}, status=400)

    total_price = sum(item.menu_item.price * item.quantity for item in cart_items)
    order = Order.objects.create(user=request.user, total_price=total_price)

    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            food_item=cart_item.menu_item,
            quantity=cart_item.quantity,
            subtotal=cart_item.menu_item.price * cart_item.quantity
        )

    cart_items.delete()  # Clear the cart
    return redirect('order_detail', order_id=order.id)

@login_required
def order_detail(request, order_id):
    # Get the order details for the specific order_id and user
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Get the items associated with the order
    order_items = order.order_items.all()
    
    # Get the user's profile and fetch all necessary details
    profile = request.user.profile
    delivery_address = profile.delivery_address
    phone_number = profile.phone_number
    state = profile.state
    country = profile.country

    # Calculate the total price if necessary
    total_price = sum(item.menu_item.price * item.quantity for item in order_items)
    
    # Pass order, order_items, delivery_address, phone_number, state, country, and total_price to the template
    return render(request, 'systemapp/order_detail.html', {
        'order': order,
        'order_items': order_items,
        'delivery_address': delivery_address,
        'phone_number': phone_number,
        'state': state,
        'country': country,
        'total_price': total_price,
    })

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'systemapp/order_list.html', {'orders': orders})

# View for order confirmation
def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'systemapp/order_confirmation.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'systemapp/order_history.html', {'orders': orders})

@login_required
def checkout(request):
    # Fetch the user's cart
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.exists():
        return redirect('view_cart')  # Redirect if the cart is empty

    if request.method == 'POST':
        # Create a new order
        order = Order.objects.create(user=request.user, total=cart.total)
        for cart_item in cart.items.all():
            # Create OrderItem for each item in the cart
            OrderItem.objects.create(
                order=order,
                food_item=cart_item.food_item,
                quantity=cart_item.quantity,
                subtotal=cart_item.quantity * cart_item.food_item.price
            )
        # Clear the cart after order is placed
        cart.items.all().delete()
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'systemapp/checkout.html', {'cart': cart})


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CustomLoginForm

# Login view
def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a page after successful login
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Please fill in all fields correctly')
    else:
        form = CustomLoginForm()

    return render(request, 'systemapp/login.html', {'form': form})

# Sign-up view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')  # Redirect to login page after sign-up
    else:
        form = UserCreationForm()
    return render(request, 'systemapp/signup.html', {'form': form})

# Logout view
def user_logout(request):
    logout(request)
    return redirect('home')

