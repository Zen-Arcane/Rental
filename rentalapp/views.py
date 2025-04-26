from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Car,User,Booking
from .serializers import CarSerializer,UserSerializer,BookingSerializer


class carViewSet(viewsets.ModelViewSet):
    queryset=Car.objects.all()
    serializer_class=CarSerializer

    #test APIS
    @action(detail=False,methods=['get'])
    def get_cars(self,request):
        name=request.query_params.get('name')
        car=Car.objects.filter(name__icontains=name,price=1313)
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


    #Update booking status
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


    


