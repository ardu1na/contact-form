from datetime import datetime
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
 
from vimacon.models import Message


def get_formatted_date(fecha):
    return datetime.strftime(fecha, "%d/%m/%Y %H:%M hs.")
    
class MessageSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=False, write_only=True)

    def validate_address(self, value):
        if value:
            raise serializers.ValidationError("You shall not pass!")
        return value

    class Meta:
        model = Message
        fields = ('asunto', 'texto', 'nombre', 'email', 'telefono', 'address')


class InboxSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = ('asunto','nombre','date','leido','spam','eliminado')
    def get_date(self, obj):
        return get_formatted_date(obj.fecha)
        

class MessageAdminSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ('asunto', 'texto', 'nombre', 'email', 'telefono','date','leido','spam','eliminado')

    def get_date(self, obj):
        return get_formatted_date(obj.fecha)


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = [ 'id','username', 'password']



"""
AUTH
"""
@api_view(['POST'])
def login(request):
    if request.user.is_authenticated:
        return Response({'message': f'You are logged in already, {request.user.username}!'}, status=status.HTTP_200_OK)
    
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("User not found", status=status.HTTP_404_NOT_FOUND)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

class LogoutView(APIView):
    
    def post(self, request):
        user = request.user
        token = get_object_or_404(Token, user=user)
        token.delete()
        return Response({'message': f'Goodbye, {user}!'}, status=status.HTTP_200_OK)



"""
FORM
"""
class MessageCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            if not serializer.validated_data.get('address'):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Spam detected."}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





"""
IBOX
"""

class InboxViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.filter(eliminado=False, spam=False)
    serializer_class = InboxSerializer  # Utilizará este serializador por defecto

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MessageAdminSerializer  # Utilizará este serializador para la vista de detalle
        return self.serializer_class

    def get_permissions(self):
        return [permissions.IsAuthenticated()]  # Requerir autenticación para otras acciones
