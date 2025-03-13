from rest_framework import serializers
from .models import Medicine, Order

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    medicine_name = serializers.ReadOnlyField(source="medicine.generic_name")
    user_name = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Order
        fields = ['id', 'user_name', 'medicine', 'medicine_name', 'quantity', 'total_price', 'status', 'order_date']
