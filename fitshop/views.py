from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, CartItem, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

# ... (keep existing imports)

# PRODUCT LIST INSIDE THE FITSHOP
def shop_home(request):
    products = Product.objects.all().order_by('id')

    # Pagination that has 6 products per page
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop_home.html', {
        'products': page_obj,     
        'page_obj': page_obj,
    })



# PRODUCT DETAIL PAGE
def product_detail(request, id):
    product = get_object_or_404(Product, id=id) # The URL used here is the slug. Slug is the text in URL that identifies the product

    return render(request, 'product_detail.html', { # Return the product detail html
        'product': product
    })


# Shows to the users all the items that exist in the cart. The non-logged in users are not able to access this functionality
@login_required(login_url="login")
def view_cart(request):

    # Fetch all cart items that belong to the current user.
    items = CartItem.objects.filter(user=request.user)

    # Calculate the total cart price by summing all subtotals.
    total_price = sum(item.subtotal for item in items)

    context = {
        "items": items,
        "total": total_price,
    }

    return render(request, "cart.html", context)


# Delete an item if the user presses the delete button
@login_required(login_url="login")
def remove_from_cart(request, item_id):
   
    # Only delete the item if it belongs to THIS user.
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()

    return redirect("view_cart")


# Adds a product only to the user's cart taht is logged in.
@login_required(login_url="login")
def add_to_cart(request, product_id):
    # Get the product the user clicked
    product = get_object_or_404(Product, id=product_id)

    # Read quantity from the form (defaults to 1 if missing)
    try:
        quantity_to_add = int(request.POST.get("quantity", 1))
        if quantity_to_add < 1:
            quantity_to_add = 1
        elif quantity_to_add > 50: # Security Limit
            quantity_to_add = 50
    except ValueError:
        quantity_to_add = 1

    # Get or create cart item for this user + product
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
    )

    if created:
        # First time this product goes into the cart:
        # set the quantity exactly to what the user chose
        cart_item.quantity = quantity_to_add
    else:
        # Product already in cart: add on top
        cart_item.quantity += quantity_to_add

    cart_item.save()

    return redirect("fitshop")  # Redirects to the view cart page


# Checkout view that redirects the user to the checkout page
@login_required
def checkout(request):
    # Get all items from the user's cart
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal for item in items)

    context = {
        'items': items,
        'total': total,
    }

    return render(request, 'checkout.html', context)


# Payment success view when the user's payment goes through
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
from paypalcheckoutsdk.orders import OrdersGetRequest
import os

def payment_success(request):
    order_id = request.GET.get('orderID')

    # Security Check: Verify order with PayPal
    client_id = "AcGV6r1y2PyR1xxDV9o5gZ0xuLKBKeScocKUk5JuXGW_7ujD5BAHxh3c4QpTtbuZGL45b53Sq6gAkhUm" # Ideally this should be in .env
    client_secret = os.getenv('PAYPAL_CLIENT_SECRET') # Must be in .env

    # Choose environment based on DEBUG or a specific setting
    environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
                  # Use LiveEnvironment for production!
    client = PayPalHttpClient(environment)

    try:
        request_obj = OrdersGetRequest(order_id)
        response = client.execute(request_obj)
        order_details = response.result
        
        if order_details.status != "COMPLETED":
             # Log this event!
             return render(request, 'fitshop/payment_error.html', {'message': 'Payment not completed'})

    except Exception as e:
        # Log error
        return render(request, 'fitshop/payment_error.html', {'message': 'Verification failed'})


    # ... Proceed with existing order creation logic ...
    
    # Send an email to the user after the transaction
    subject = "Thank You for Your Purchase! Your Order is Confirmed"
    message = (
        f"Hello {request.user.first_name or request.user.username},\n\n"
        f"Thank you for shopping with FitTrack! We're excited to let you know that your order has been successfully processed and confirmed.\n\n"
        f"Here are the details of your purchase:\n\n"
        f"Order ID: {order_id}\n"
        f"Your items will be shipped soon, and you will receive a notification once they are on their way. You can always track your order in your account.\n\n"
        f"If you have any questions or need assistance, don't hesitate to reply to this email. We're here to help!\n\n"
        f"Thank you for choosing FitTrack, and we hope you enjoy your purchase!\n\n"
        f"The FitTrack Team"
    )

    send_mail(
        subject,
        message,
        "fittrack.services@gmail.com",     
        [request.user.email],           
        fail_silently=False,
    )

    # --- SAVE ORDER HISTORY ---
    # Fetch all cart items that belong to the current user
    user_cart_items = CartItem.objects.filter(user=request.user)
    
    if user_cart_items.exists():
        # Calculate total price again to be safe
        total_price = sum(item.subtotal for item in user_cart_items)
        
        # Verify total matches paid amount (Optional but recommended)
        # if float(order_details.purchase_units[0].amount.value) != float(total_price):
             # handle Mismatch

        # Create the Order record
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            order_id=order_id
        )
        
        # Save each item
        for item in user_cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity
            )

    # Clear the user's cart after successful payment
    user_cart_items.delete()  # This will delete all items from the user's cart

    # Process order or save the payment details here
    return render(request, 'payment_success.html', {'order_id': order_id})



# View that handles the clerance of the cart when user ends his payment
def clear_cart(request):
    if request.method == "POST" and request.user.is_authenticated:
        user_cart_items = CartItem.objects.filter(user=request.user)
        user_cart_items.delete()  # Delete all items from the user's cart
        return JsonResponse({"status": "success"}, status=200)
    return JsonResponse({"status": "error"}, status=400)


# Order Detail View
@login_required(login_url="login")
def order_detail(request, id):
    # Fetch the order and ensure it belongs to the logged-in user
    order = get_object_or_404(Order, id=id, user=request.user)
    
    return render(request, 'order_detail.html', {
        'order': order
    })