from rest_framework import serializers
from .models import User, ParkingSpace, Reservation, Vehicle
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone_number']

    class RegisterSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True, required=True, validators=[validate_Password])
        password2 = serializers.Charfield(write_only=True, required=True)

        class Meta:
            model = User
            fields = ['username', 'email', 'password', 'password2', 'role', 'phone_number']    

        def validate(self, data):
            if data['password'] != data['password2']:
                raise serializers.ValidationError({"password": "Passwords must match."})
            return data

        def create(self, validated_data):
            validated_data.pop('password2')  
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                role=validated_data.get('role', 'driver'),
                phone_number=validated_data.get('phone_number', '')
            )  
            return user

class ParkingLotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingLot
        fields = ['id', 'name', 'location', 'capacity', 'description']

class ParkingSpaceSerializer(serializers.ModelSerializer):
    is_taken = serializers.SerializerMethodField()

    class Meta:
        model = ParkingSpace
        fields = ['id', 'parking_lot', 'space_number', 'status', 'is_active', 'is_taken'] 

    def get_is_taken(self, obj):
        return obj.is_taken()           