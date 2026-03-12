from django.urls import path
from .views import FoodListView, FoodDetailView, create_order,kitchen_dashboard,kitchen_orders,update_order_status

from .views import OrderCreateView

urlpatterns = [
    path('api/food/', FoodListView.as_view()),
    path('api/food/<int:pk>/', FoodDetailView.as_view()),
    path('api/orders/', OrderCreateView.as_view()),
    path("api/kitchen/orders/", kitchen_orders),
    path("kitchen/", kitchen_dashboard),
    path("api/order/<int:order_id>/status/", update_order_status),
]