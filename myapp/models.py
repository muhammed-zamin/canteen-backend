from django.db import models

class FoodItem(models.Model):
    TYPE_CHOICES = [
        ("veg", "Veg"),
        ("nonveg", "Non-Veg"),
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    is_available = models.BooleanField(default=True)

    # ✅ NEW FIELD
    food_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="veg")

    def __str__(self):
        return self.name


status_choices = [
    ("pending", "Pending"),
    ("cooking", "Cooking"),
    ("ready", "Ready"),
    ("served", "Served")
]

class Order(models.Model):
    table_number = models.IntegerField()
    customer_name = models.CharField(max_length=100, default="Guest")
    order_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=status_choices, default="pending")
    total_price = models.FloatField(default=0)

    def __str__(self):
        return f"Order {self.id} - Table {self.table_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.food_item.name} x {self.quantity}"