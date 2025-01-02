from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant, MenuItem, Order,OrderItem,  Cart
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    return render(request, 'systemapp/home.html')

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'systemapp/restaurant_list.html', {'restaurants': restaurants})

def menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = restaurant.menuitem_set.all()
    return render(request, 'systemapp/menu.html', {'restaurant': restaurant, 'menu_items': menu_items})

# View for adding items to the cart
def add_to_cart(request, item_id):
    item = MenuItem.objects.get(id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.menu_items.add(item)
    cart.total_price += item.price
    cart.save()
    return redirect('cart')

# View for viewing the cart
def view_cart(request):
    cart = Cart.objects.get(user=request.user)
    return render(request, 'systemapp/view_cart.html', {'cart': cart})

@login_required
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = cart.items.filter(id=item_id).first()

    if cart_item:
        cart_item.delete()  # Remove the item from the cart

    return redirect('view_cart')  # Redirect to the cart page

# View for placing an order

@login_required
def place_order(request):
    # Get the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    total_price = sum(item.menu_item.price for item in cart.cart_items.all())
    # Create a new order
    order = Order.objects.create(
        user=request.user,
        total_price=cart.total_price,
        delivery_status='Pending'
    )

    # Add menu items from the cart to the order
    order.menu_items.set(cart.menu_items.all())

    # Save the order
    order.save()

    # Create a payment for the order (simplified for now)
    Payment.objects.create(
        order=order,
        payment_method="Credit Card",  # Simplified, adjust based on actual payment method
        payment_status="Pending"
    )

    # Clear the cart after placing the order
    cart.menu_items.clear()
    cart.total_price = 0
    cart.save()

    # Redirect to the order confirmation page
    return redirect('order_confirmation', order_id=order.id)

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

