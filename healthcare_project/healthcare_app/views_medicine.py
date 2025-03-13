from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Medicine, Order
from .serializers import MedicineSerializer, OrderSerializer

@api_view(['GET'])
def medicine_list(request):
    medicines = Medicine.objects.all()
    serializer = MedicineSerializer(medicines, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Only authenticated users can place orders
def place_order(request):
    medicine_id = request.data.get('medicine_id')
    quantity = int(request.data.get('quantity', 1))

    try:
        medicine = Medicine.objects.get(id=medicine_id)
    except Medicine.DoesNotExist:
        return Response({"error": "Medicine not found"}, status=404)

    total_price = medicine.price_range  # Keeping it simple, using price range as string

    order = Order.objects.create(
        user=request.user,
        medicine=medicine,
        quantity=quantity,
        total_price=total_price,
        status='pending'
    )

    return Response({"message": "Order placed successfully!", "order_id": order.id}, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
