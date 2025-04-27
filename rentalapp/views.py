from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Car,User,Booking
from .serializers import CarSerializer,UserSerializer,BookingSerializer
from django.utils import timezone 


class carViewSet(viewsets.ModelViewSet):
    queryset=Car.objects.all()
    serializer_class=CarSerializer

    #test APIS
    @action(detail=False,methods=['get'])
    def get_cars(self,request):
        name=request.query_params.get('name')
        car=Car.objects.filter(name__icontains=name)
        return Response(CarSerializer(car,many=True).data)
    
    #test APIS
    @action(detail=False, methods=['get'])
    def get_status(self, request):
        cars = Car.objects.filter(is_available=True)
        return Response(CarSerializer(cars, many=True).data)

    #update available status
    @action(detail=True,methods=['post'])   
    def update_availability(self,request,pk=None):

        car=self.get_object()
        is_available=request.data.get('is_available',car.is_available)

        if not isinstance(is_available, bool):
            return Response({"error": "is_available must be a boolean."}, status=400)
        
        car.is_available=is_available
        car.save()
        return Response(CarSerializer(car).data)
    
class bookingViewSet(viewsets.ModelViewSet):
    queryset=Booking.objects.all()
    serializer_class=BookingSerializer

    #create booking
    @action(detail=False,methods=['post'])
    def create_booking(self,request,pk=None):
        car_id=request.data.get('car_id')
        user_id=request.data.get('user_id')
        start_date=request.data.get('start_date')
        end_date=request.data.get('end_date')

        try:
            car=Car.objects.get(id=car_id)
            if not car.is_available:
                    return Response({"error": "Car is not available."}, status=400)
        except Car.DoesNotExist:
            return Response({"error": "Car not found."}, status=400)
        
        booking_date=timezone.now()
        
        booking=Booking.objects.create(
            car=car,
            user=user_id,
            start_date=start_date,
            end_date=end_date,
            booking_date=booking_date,
            is_confirmed=False,
            is_cancelled=False,

        )
        car.is_available=False
        car.save()

        return Response({
            "message": "Booking created successfully.",
            "booking": BookingSerializer(booking).data
        }, status=201)
    

    #Update booking status for confirming
    @action(detail=True,methods=['post'])
    def confirm_booking(self,request,pk=None):
        booking=self.get_object()

        if booking.is_confirmed:
            return Response({"error": "Booking already confirmed."}, status=400)
        
        booking.is_confirmed=True
        booking.save()

        car=booking.car
        car.is_available=False
        car.save()
    
        return Response({
            "message": "Booking confirmed successfully.",
            "booking": BookingSerializer(booking).data
        })
    
class userViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer

    #test APIS
    @action(detail=False,methods=['get'])
    def get_user(self,request):
        user=request.query_params.get('user')
        users=User.objects.filter(user__icontains=user)
        if users:
            return Response(UserSerializer(users,many=True).data)
        return Response({"error":"user not found"},status=404)  


    #test APIS
    @action(detail=False, methods=['get'])
    def get_user_phone_by_name(self, request):
        name = request.query_params.get('user')
        user = User.objects.filter(user=name).first()
        if user:
            return Response({"phone": user.phone})
        return Response({"error": "User not found"}, status=404)


    


