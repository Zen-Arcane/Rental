from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Car,User,Booking
from .serializers import CarSerializer,UserSerializer,BookingSerializer,UserProfileSerializer
from django.utils import timezone 
from django.contrib.auth.hashers import check_password

class carViewSet(viewsets.ModelViewSet):
    queryset=Car.objects.all()
    serializer_class=CarSerializer

    #test APIS
    @action(detail=False,methods=['get'])
    def get_cars_by_name(self,request):
        name=request.query_params.get('name')
        car=Car.objects.filter(name__icontains=name)
        return Response(CarSerializer(car,many=True).data)
    
    @action(detail=False,methods=['get'])
    def get_cars(self,request):
        brand=request.query_params.get('brand')
        car=Car.objects.filter(brand__icontains=brand)
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
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=400)
        
        booking_date=timezone.now()

        if Booking.objects.filter(car=car, user=user).exists():
            return Response({"error": "Booking already exists."}, status=400)

        
        booking=Booking.objects.create(
            car=car,
            user=user,
            start_date=start_date,
            end_date=end_date,
            booking_date=booking_date,
            is_confirmed=False,
            is_cancelled=False,

        )
        car.save()

        return Response({
            "message": "Booking created successfully.",
            "booking": BookingSerializer(booking).data
        }, status=201)
    

    @action(detail=False,methods=['post'])
    def delete_booking(self,request):
        booking_id=request.query_params.get('id')
        if not booking_id:
                return Response({"error":"Booking id not found."},status=400)

        booking=Booking.objects.filter(id=booking_id).first()
        if not booking:
            return Response({"error":"Booking doesnot exist."},status=400)
        
        booking.delete()
        return Response({"Success":"Booking deleted"},status=200)

    @action(detail=False,methods=['post'])
    def cancel_booking(self,request):
        booking_id=request.query_params.get('id')

        if not booking_id:
            return Response({"error":"Booking id not found."},status=400)
        booking=Booking.objects.filter(id=booking_id).first()
        if not booking:
            return Response({"error": "Booking does not exist."}, status=400)
        
        booking.is_cancelled=True
        booking.is_confirmed=False
        booking.save()

        return Response({"success":"Booking Cancelled."},status=200)
    
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
    
    @action(detail=False,methods=['get'])
    def get_bookings_user(self,request,pk=None):
        user_id=request.query_params.get('user_id')

        try:
            user=User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "No bookings found for user."}, status=400)
        
        booking=Booking.objects.filter(user=user)
        if not booking.exists():
            return Response({"error": "No bookings found for user."}, status=400)
    
        return Response(BookingSerializer(booking, many=True).data)
    
class userViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer

    #test APIS
    @action(detail=False,methods=['get'])
    def get_user(self,request):
        user=request.query_params.get('user')
        users=User.objects.filter(user__icontains=user)
        if users:
            return Response(UserProfileSerializer(users,many=True).data)
        return Response({"error":"user not found"},status=404)  
    

    @action(detail=False,methods=['post'])
    def delete_user(self,request):
        user=request.query_params.get('id')
        if not user:
            return Response({"error":"Id not found"},status=400)
        
        users=User.objects.filter(id=user)

        if not users:
            return Response({"error":"User Doesnot exist"},status=400)
        
        users.delete()
        
        return Response({"Success":"User Deleted Successfully"},status=200)
       


    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('user')
        password = request.data.get('pass')

        if not username or not password:
            return Response({"error": "Username and password required."}, status=400)

        try:
            user = User.objects.get(user=username)
            print(password,user.passwd)
            if check_password(password, user.passwd):
                return Response({"id": user.id, "success": "User Found"}, status=200)
            else:
                return Response({"error": "Invalid password"}, status=400)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=400)
    #test APIS
    @action(detail=False, methods=['get'])
    def get_user_phone_by_name(self, request):
        name = request.query_params.get('user')
        user = User.objects.filter(user=name).first()
        if user:
            return Response({"phone": user.phone})
        return Response({"error": "User not found"}, status=404)


    


