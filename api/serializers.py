from rest_framework import serializers
from .models import User, ParkingSpace, Reservation, Vehicle
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone_number']

    class RegisterSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True, required=True, validators=[validate_Password])
        password2 = serializers.CharField(write_only=True, required=True)

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

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'user', 'license_plate', 'vehicle_type']
        read_only_fields = ['user']
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'vehicle', 'space', 'start_time', 'end_time', 'status', 'created_at']
        read_only_fields = ['user', 'status', 'created_at']

    def validate(self, data):
        space = data['space']
        start_time = data['start_time']
        end_time = data['end_time']

        if start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time.")

        if space.status != 'available':
            raise serializers.ValidationError("This space is not available.")

        if Reservation.objects.filter(space=space, status='booked').exists():
            raise serializers.ValidationError("A reservation already exists for this space.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user

        space = validated_data['space']
        space.status = 'reserved'
        space.save()

        reservation = Reservation.objects.create(**validated_data)
        return reservation