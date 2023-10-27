from rest_framework.serializers import ModelSerializer
from .models import message,chat_user


class postSerializer(ModelSerializer):
    class Meta:
        model = message
        fields = '__all__'
        
class chatUserSerializer(ModelSerializer):
    class Meta:
        model = chat_user
        fields = '__all__'
        