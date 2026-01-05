from django.shortcuts import render, redirect, get_object_or_404
from .models import Food, Consume

# Main MyCals page (add and list foods)
def mycals_view(request):

    # Block access if the user is not logged in
    if not request.user.is_authenticated:
        return render(request, "mycals.html", {"auth_required": True})

    error_message = None

    # Handle adding a new food
    if request.method == "POST":
        query = (request.POST.get("food_consumed") or "").strip()

        if query:

            # Tries several matching methods for better results and convenience
            food = (
                Food.objects.filter(name__iexact=query).first()
                or Food.objects.filter(name__istartswith=query).first()
                or Food.objects.filter(name__icontains=query).first()
            )

            if food:

                # Save the entry
                Consume.objects.create(user=request.user, food_consumed=food)
                return redirect("mycals")

            else:
                # Show an error ONLY for this POST
                error_message = f"'{query}' was not found. Please try adding a different food."

    # Load today's consumed items
    consumed_food = (
        Consume.objects.filter(user=request.user)
        .select_related("food_consumed")
        .order_by("-date", "-id")
    )

    context = {"consumed_food": consumed_food}

    if error_message:
        context["error_message"] = error_message  

    return render(request, "mycals.html", context)

# Delete a food entry
def delete_food(request, pk):
    item = get_object_or_404(Consume, pk=pk, user=request.user)
    item.delete()
    return redirect("mycals")
