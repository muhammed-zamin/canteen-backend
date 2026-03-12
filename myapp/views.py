from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("MyApp is working")

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from .models import FoodItem
from .serializers import FoodItemSerializer

from .models import Order
from .serializers import OrderSerializer
from .serializers import KitchenOrderSerializer
from django.shortcuts import render




@api_view(["POST"])
@csrf_exempt
def update_order_status(request, order_id):

    order = Order.objects.get(id=order_id)
    status = request.data.get("status")

    order.status = status
    order.save()

    return Response({"message": "Status updated"})

def kitchen_dashboard(request):
    return render(request, "kitchen.html")

@api_view(["GET"])
def kitchen_orders(request):
    orders = Order.objects.all()
    serializer = KitchenOrderSerializer(orders, many=True)
    return Response(serializer.data)


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class FoodListView(generics.ListCreateAPIView):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer

class FoodDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer

from django.http import JsonResponse
from .models import Order

def create_order(request):
    table_number = request.GET.get("table")

    order = Order.objects.create(
        customer_name="Guest",
        table_number=table_number
    )

    return JsonResponse({
        "message": "Order created",
        "table": table_number
    })