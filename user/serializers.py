#not in use
from rest_framework import serializers
from .models import deliever,Orderdetail
class delieverSerializer(serializers.Serializer):
    class Meta:
        model=deliever
        fields='__all__'

class OrderdetailSerializer(serializers.Serializer):
    class Meta:
        model=Orderdetail
        fields='__all__'
