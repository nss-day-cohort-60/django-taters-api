from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Category


class CategoryView(ViewSet):

    def list(self, request):

        categories = Category.objects.all()
        serialized = CategorySerializer(categories, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try: 
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist: 
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        serialized = CategorySerializer(category, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        category = Category.objects.create(
            label = request.data['label']
        )
        
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'label', )
