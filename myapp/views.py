from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

from django.db.models import Sum, F

from .models import FoodItem, Order, OrderItem
from .serializers import FoodItemSerializer, OrderSerializer, KitchenOrderSerializer

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny

# 🔹 Home
def home(request):
    return HttpResponse("MyApp is working")


# 🔹 Sales Page
def sales_page(request):
    return render(request, "sales.html")
#   menu management page
def manage_menu(request):
    return render(request, "manage_menu.html")

# 🔹 Sales API (with date filter)
@api_view(["GET"])
def sales_data(request):
    date = request.GET.get("date")

    if date:
        selected_date = datetime.strptime(date, "%Y-%m-%d").date()
        orders = Order.objects.filter(order_time__date=selected_date, status="served")
    else:
        orders = Order.objects.filter(status="served")

    total_orders = orders.count()

    total_sales = (
        OrderItem.objects
        .filter(order__in=orders)
        .aggregate(total=Sum(F("quantity") * F("food_item__price")))
    )["total"] or 0

    return Response({
        "orders": total_orders,
        "sales": total_sales
    })


# 🔹 Order Status (for frontend progress bar)
@api_view(["GET"])
def get_order_status(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        return Response({
            "order_id": order.id,
            "status": order.status
        })
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)


# 🔹 Update Order Status (kitchen)
@api_view(["POST"])
@csrf_exempt
def update_order_status(request, order_id):
    order = Order.objects.get(id=order_id)
    status = request.data.get("status")

    order.status = status
    order.save()

    return Response({"message": "Status updated"})


# 🔹 Kitchen Dashboard
def kitchen_dashboard(request):
    return render(request, "kitchen.html")


# 🔹 Kitchen Orders (NEWEST FIRST ✅)
@api_view(["GET"])
def kitchen_orders(request):
    orders = Order.objects.all().order_by("-order_time")
    serializer = KitchenOrderSerializer(orders, many=True)
    return Response(serializer.data)


# 🔹 Create Order API
class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


# 🔹 Food APIs
class FoodListView(generics.ListCreateAPIView):
    
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    authentication_classes = []   # 🚨 disable auth
    permission_classes = [AllowAny] 


class FoodDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@csrf_exempt
@api_view(["POST"])
@authentication_classes([])   # 🚨 disables session auth (important)
@permission_classes([AllowAny]) 



@api_view(["POST"])
@csrf_exempt
def toggle_availability(request, food_id):
    try:
        item = FoodItem.objects.get(id=food_id)
        item.is_available = not item.is_available
        item.save()

        return Response({
            "message": "Availability updated",
            "is_available": item.is_available
        })

    except FoodItem.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)