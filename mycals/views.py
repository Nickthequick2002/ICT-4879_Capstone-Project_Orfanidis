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
        quantity = float(request.POST.get("quantity") or 1.0)

        if query:

            # Tries several matching methods for better results and convenience
            food = (
                Food.objects.filter(name__iexact=query).first()
                or Food.objects.filter(name__istartswith=query).first()
                or Food.objects.filter(name__icontains=query).first()
            )

            if not food:
                # API Fallback (OpenFoodFacts)
                import requests
                try:
                    url = "https://world.openfoodfacts.org/cgi/search.pl"
                    params = {
                        "search_terms": query,
                        "search_simple": 1,
                        "action": "process",
                        "json": 1,
                        "page_size": 1
                    }
                    response = requests.get(url, params=params, timeout=5)
                    data = response.json()
                    
                    if data.get("products"):
                        product = data["products"][0]
                        nutriments = product.get("nutriments", {})
                        
                        # Extract data (defaulting to 0 if missing)
                        name = product.get("product_name", query)
                        calories = float(nutriments.get("energy-kcal_100g", 0) or 0)
                        protein = float(nutriments.get("proteins_100g", 0) or 0)
                        carbs = float(nutriments.get("carbohydrates_100g", 0) or 0)
                        fats = float(nutriments.get("fat_100g", 0) or 0)
                        
                        # Create new Food item (cached from API)
                        food = Food.objects.create(
                            name=name,
                            calories=calories,
                            protein=protein,
                            carbs=carbs,
                            fats=fats,
                            serving_qty=100, # API standards are usually per 100g
                            serving_unit="g"
                        )
                except Exception as e:
                    print(f"API Error: {e}")

            if food:

                # Save the entry
                Consume.objects.create(user=request.user, food_consumed=food, quantity=quantity)
                return redirect("mycals")

            else:
                # Show an error ONLY for this POST
                error_message = f"'{query}' was not found locally or in the global database. Please try a different food."

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
