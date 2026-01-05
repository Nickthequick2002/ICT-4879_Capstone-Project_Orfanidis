from .models import CartItem

#This view is created to make dynamically update the cart icon page on how many products are inside it
def cart_item_count(request):
    if request.user.is_authenticated:
        # Count ONLY unique cart items, not their quantities
        return {
            "cart_count": CartItem.objects.filter(user=request.user).count()
        }
    else:
        return {"cart_count": 0}