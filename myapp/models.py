
# from django.db import models

# class Order(models.Model):
#     CANCEL_CHOICES = [
#         ('non-cancel', 'Non-Cancel'),
#         ('cancel', 'Cancel'),
#     ]

#     id_name = models.CharField(max_length=50)
#     timing = models.TimeField()
#     date = models.DateField()
#     order_id = models.CharField(max_length=50)
#     amount = models.IntegerField()
#     address_code = models.CharField(max_length=50)
#     cancel_status = models.CharField(max_length=20, choices=CANCEL_CHOICES, default='non-cancel')

#     def __str__(self):
#         return f"Order {self.order_id}"


from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    CANCEL_CHOICES = [
        ('non-cancel', 'Non-Cancel'),
        ('cancel', 'Cancel'),
    ]
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    id_name = models.CharField(max_length=50)
    timing = models.TimeField()
    date = models.DateField()
    order_id = models.CharField(max_length=500)
    amount = models.IntegerField()
    address_code = models.CharField(max_length=50)
    refresh_link = models.CharField(max_length=200)  # New field
    cancel_status = models.CharField(max_length=20, choices=CANCEL_CHOICES, default='non-cancel')


    def __str__(self):
            return f"Order {self.order_id} by {self.user.username}"



class OrderLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)  # e.g., "created", "updated", "deleted"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.action} order {self.order.order_id} at {self.timestamp}"




