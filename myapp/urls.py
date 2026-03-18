from django.urls import path
from .views import FoodListView, FoodDetailView , kitchen_dashboard,kitchen_orders,update_order_status,get_order_status, toggle_availability,manage_menu
from . import views
from .views import OrderCreateView
from .views import sales_page, sales_data, get_order_status

urlpatterns = [
    
    path("api/order/<int:order_id>/", get_order_status),
    path('api/food/', FoodListView.as_view()),
    path('api/food/<int:pk>/', FoodDetailView.as_view()),
    path('api/orders/', OrderCreateView.as_view()),
    path("api/kitchen/orders/", kitchen_orders),
    path("kitchen/", kitchen_dashboard),
    path("api/order/<int:order_id>/status/", update_order_status),
    path("kitchen/sales-page/", sales_page),
    path("api/kitchen/sales/", sales_data),
    path("api/food/<int:food_id>/toggle/", toggle_availability),
    path("kitchen/manage-menu/", manage_menu),
    
    
]
"""Menu:

http://127.0.0.1:8000/myapp/api/food/

Kitchen:

http://127.0.0.1:8000/myapp/kitchen/

Sales page:

http://127.0.0.1:8000/myapp/kitchen/sales-page/

Sales API:

http://127.0.0.1:8000/myapp/api/kitchen/sales/?date=2026-03-17
"""