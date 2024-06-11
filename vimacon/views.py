from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from vimacon.models import Message

class MessageSerializer(serializers.ModelSerializer):
    honeypot = serializers.CharField(required=False, write_only=True)

    def validate_honeypot(self, value):
        if value:
            raise serializers.ValidationError("You shall not pass!")
        return value

    class Meta:
        model = Message
        fields = ('asunto', 'texto', 'nombre', 'email', 'telefono', 'honeypot')



class MessageCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            if not serializer.validated_data.get('honeypot'):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Spam detected."}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)