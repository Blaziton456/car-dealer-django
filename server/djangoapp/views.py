import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from dealership.models import Dealer
from django.shortcuts import render, redirect
from dealership.models import Dealer, DealerReview



@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("userName")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                "userName": user.username
            })

        return JsonResponse({
            "userName": ""
        }, status=401)

    return JsonResponse({
        "error": "POST request required"
    }, status=405)

def logout_user(request):
    logout(request)
    return JsonResponse({
        "userName": ""
    })

from dealership.models import DealerReview


def get_dealer_reviews(request, dealer_id):
    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse({"error": "Dealer not found"}, status=404)

    reviews = DealerReview.objects.filter(dealer_id=dealer_id)

    if "text/html" in request.headers.get("Accept", ""):
        return render(
            request,
            "dealer_reviews.html",
            {
                "dealer": dealer,
                "reviews": reviews
            }
        )

    if request.method == "GET":
        data = []

        for review in reviews:
            data.append({
                "id": review.id,
                "dealer_id": review.dealer_id,
                "dealership": review.dealership,
                "name": review.name,
                "purchase": review.purchase,
                "review": review.review,
                "purchase_date": review.purchase_date,
                "car_make": review.car_make,
                "car_model": review.car_model,
                "car_year": review.car_year,
                "sentiment": review.sentiment
            })

        return JsonResponse(data, safe=False)

    return JsonResponse(
        {"error": "GET request required"},
        status=405
    )

def get_all_dealers(request):
    if request.method == "GET":
        dealers = Dealer.objects.all()

        data = []

        for dealer in dealers:
            data.append({
                "state": dealer.state,
                "address": dealer.address,
                "zip": dealer.zip,
                "latitude": dealer.latitude,
                "longitude": dealer.longitude,
                "short_name": dealer.short_name,
                "full_name": dealer.full_name
            })

        return JsonResponse(data, safe=False)

    return JsonResponse({"error": "GET request required"}, status=405)

def get_dealer_by_id(request, dealer_id):
    if request.method == "GET":
        try:
            dealer = Dealer.objects.get(id=dealer_id)

            data = {
                "state": dealer.state,
                "address": dealer.address,
                "zip": dealer.zip,
                "latitude": dealer.latitude,
                "longitude": dealer.longitude,
                "short_name": dealer.short_name,
                "full_name": dealer.full_name
            }

            return JsonResponse(data)

        except Dealer.DoesNotExist:
            return JsonResponse({"error": "Dealer not found"}, status=404)

    return JsonResponse({"error": "GET request required"}, status=405)

def get_dealers_by_state(request, state):
    dealers = Dealer.objects.filter(state__iexact=state)

    if "text/html" in request.headers.get("Accept", ""):
        return render(
            request,
            "state_dealers.html",
            {
                "dealers": dealers,
                "state": state
            }
        )

    if request.method == "GET":
        data = []

        for dealer in dealers:
            data.append({
                "state": dealer.state,
                "address": dealer.address,
                "zip": dealer.zip,
                "latitude": dealer.latitude,
                "longitude": dealer.longitude,
                "short_name": dealer.short_name,
                "full_name": dealer.full_name
            })

        return JsonResponse(data, safe=False)

    return JsonResponse(
        {"error": "GET request required"},
        status=405
    )

def get_all_car_makes(request):
    if request.method == "GET":
        car_makes = [
            {
                "make": "Toyota",
                "models": ["Camry", "Corolla", "RAV4"]
            },
            {
                "make": "Honda",
                "models": ["Civic", "Accord", "CR-V"]
            },
            {
                "make": "Ford",
                "models": ["Mustang", "F-150", "Explorer"]
            },
            {
                "make": "BMW",
                "models": ["3 Series", "5 Series", "X5"]
            }
        ]

        return JsonResponse(car_makes, safe=False)

    return JsonResponse({"error": "GET request required"}, status=405)

def analyze_review(request, review_text):
    if request.method == "GET":
        sentiment = "Positive"

        return JsonResponse({
            "review": review_text,
            "sentiment": sentiment
        })

    return JsonResponse({"error": "GET request required"}, status=405)

from django.shortcuts import render

def home(request):
    return render(request, "index.html")


def review_dealer(request, dealer_id):
    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse({"error": "Dealer not found"}, status=404)

    if request.method == "POST":
        DealerReview.objects.create(
            dealer_id=dealer.id,
            dealership=dealer.full_name,
            name=request.POST.get("name"),
            purchase=True if request.POST.get("purchase") else False,
            review=request.POST.get("review"),
            purchase_date=request.POST.get("purchase_date"),
            car_make=request.POST.get("car_make"),
            car_model=request.POST.get("car_model"),
            car_year=int(request.POST.get("car_year")),
            sentiment="Positive"
        )

        return redirect(f"/dealer/{dealer.id}/reviews")

    return render(
        request,
        "review_dealer.html",
        {
            "dealer": dealer
        }
    )