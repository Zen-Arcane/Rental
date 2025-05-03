from django.db import models

class Car(models.Model):
        name = models.CharField(max_length=100)
        brand = models.CharField(max_length=100)
        description=models.TextField()
        price = models.DecimalField(max_digits=8,decimal_places=2)
        is_available = models.BooleanField(default=True)
        created_at=models.DateTimeField(auto_now_add=True)
        rating=models.DecimalField(max_digits=2,decimal_places=1)
<<<<<<< HEAD
        image = models.ImageField(upload_to='uploads/')
=======
        image=models.TextField()
>>>>>>> 3d99e6dd25344f98355d82ecf252731cf8668796
        video_url=models.TextField()

        def __str__(self):
            return self.name
class User(models.Model):
        user=models.CharField(max_length=100)
        phone=models.CharField(max_length=10)
        email=models.EmailField()
        passwd=models.CharField(max_length=255) 

        def __str__(self):
           return self.user
             
class Booking(models.Model):
        car=models.ForeignKey(Car,related_name="bookings", on_delete=models.CASCADE)
        user = models.ForeignKey(User, related_name="bookings", on_delete=models.CASCADE)
        start_date=models.DateField()
        end_date=models.DateField()
        booking_date=models.DateTimeField(default='2025-04-01 00:00:00')
        is_confirmed=models.BooleanField(default=False)
        is_cancelled=models.BooleanField(default=False)

        def __str__(self):
                return f"{self.user},{self.car.name}"

