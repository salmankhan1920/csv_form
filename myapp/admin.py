from django.contrib import admin
from .models import Order, OrderLog

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'id_name', 'date', 'timing', 'amount', 'cancel_status')
    list_filter = ('cancel_status', 'date')
    search_fields = ('order_id', 'id_name', 'user__username')
    readonly_fields = ('timing', 'date')

@admin.register(OrderLog)
class OrderLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'action', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'order__order_id')
    readonly_fields = ('timestamp',)

