from rest_framework import serializers

from product.serializers import ProductListSerializer 
from .models import Category


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = ('slug', 'name')


class CategoryDetailSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    class Meta:
        model = Category 
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['products'] = ProductListSerializer(instance.products.all(), many=True).data 
        return representation