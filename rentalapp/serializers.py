from rest_framework import serializers
from .models import Car,User,Booking

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model=Car
        fields=['id','name','description','price','is_available','created_at','image']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','user','phone','email']
class BookingSerializer(serializers.ModelSerializer):

    car_details = CarSerializer(source='car', read_only=True)
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model=Booking
        fields=['id','car','user','start_date','end_date','booking_date','is_confirmed','is_cancelled','car_details','user_details']



      