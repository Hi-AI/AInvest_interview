from rest_framework import serializers
from user.models import *

class UserInfoSerializer(serializers.ModelSerializer):
    '''创建序列化器'''
    class Meta:
        model = User  
        fields = '__all__' 
     
class PSerializer(serializers.ModelSerializer):
    '''创建序列化器'''
    class Meta:
        model = User  
        fields = '__all__' 
     
