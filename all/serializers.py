from rest_framework import serializers
from .models import Object, Apartment, User


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = '__all__'


class ApartmentSerializer(serializers.ModelSerializer):
    object_name = serializers.CharField(source='object.name', read_only=True)

    class Meta:
        model = Apartment
        fields = [
            'id', 'object', 'object_name', 'room_number', 'rooms', 'area', 'floor',
            'price', 'status', 'description', 'secret_code'
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'fio', 'address', 'phone_number', 'object_id', 'apartment_id',
            'user_type', 'telegram_chat_id', 'balance', 'kafil_fio', 'kafil_address',
            'kafil_phone_number', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance