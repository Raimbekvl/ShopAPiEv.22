from rest_framework.viewsets import ModelViewSet 
from rest_framework import permissions, response
from rest_framework.decorators import action
from rating.serializers import ReviewSerializer
from .import serializers
from .models import Product



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action =='list':
            return serializers.ProductListSerializer
        return serializers.ProductDetailSerializer

    #api/v1/products/<id>/reviews/
    @action(['GET', 'POST'], detail=True)
    def reviews(self, request, pk=None):
        product = self.get_object()
        if request.method == 'GET':
            reviews = product.reviews.all()
            serializer = ReviewSerializer(reviews, many=True).data
            return response.Response(serializer, status=200)
        data = request.data 
        serializer = ReviewSerializer(data=data, context={'request': request, 'product': product})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=201)

    def get_permissions(self):
        #Создавать посты может залогинкнный юзер
        if self.action in ('create', 'add_to_liked', 'remove_from_liked', 'favorite_action'):
            return [permissions.IsAuthenticated()]
        #Изменять и удалять может только автор поста
        elif self.action in ('update', 'partial_update', 'destroy', 'get_likes'):
            return [permissions.IsAuthenticated(),]
        # Просматривать могут все
        else:
            return [permissions.AllowAny(),]

    