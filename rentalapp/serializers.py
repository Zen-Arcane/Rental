from rest_framework import serializers
from .models import Car,User,Booking
from django.contrib.auth.hashers import make_password

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model=Car
        fields=['id','name','brand','description','price','is_available','created_at','rating','image','video_url']

class UserSerializer(serializers.ModelSerializer):
    passwd = serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=['id','user','phone','email','passwd']

    def create(self, validated_data):
        validated_data['passwd'] = make_password(validated_data['passwd'])
        return super().create(validated_data)
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user', 'email', 'phone']

class BookingSerializer(serializers.ModelSerializer):

    car_details = CarSerializer(source='car', read_only=True)
    user_details = UserProfileSerializer(source='user', read_only=True)

    class Meta:
        model=Booking
        fields=['id','car','user','start_date','end_date','booking_date','is_confirmed','is_cancelled','car_details','user_details']



      