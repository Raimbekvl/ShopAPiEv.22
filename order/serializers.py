from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemsSerializer(serializers.ModelSerializer):
    product_title = serializers.ReadOnlyField(source='product.title')
    

    class Meta:
        # product = serializers.ReadOnlyField(source='product.title')
        model = OrderItem 
        fields = ('product', 'quantity', 'product_title')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr.pop('product')
        return repr



class OrderSerializer(serializers.ModelSerializer):
    positions = OrderItemsSerializer(write_only=True, many=True)
    status = serializers.CharField(read_only=True)
    user = serializers.ReadOnlyField(source='user.email')
    class Meta:
        model = Order
        fields = ('id', 'user', 'created_at', 'positions', 'status')
    
    def create(self, validated_data):
        products = validated_data.pop('positions')
        user = self.context.get('request').user
        order = Order.objects.create(user=user, status='open')
        for prod in products:
            product = prod['product']
            quantity = prod['quantity']
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
        return order

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['products'] = OrderItemsSerializer(instance.items.all(), many=True).data
        return repr