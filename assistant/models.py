# models.py
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    dominant_color = models.CharField(max_length=50, blank=True)
    predicted_style = models.TextField(blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='F')

    def __str__(self):
        return f'{self.user.username} Profile'


class ClothingItem(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='clothes')
    image = models.ImageField(upload_to='clothes/')
    description = models.TextField(blank=True)
    predicted_style = models.CharField(max_length=100, blank=True)
    fine_category = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Clothing Item for {self.profile.user.username}'

class UserOutfit(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_outfits')
    image = models.ImageField(upload_to='outfits/')
    description = models.TextField()
    predicted_style = models.CharField(max_length=100)
    detected_labels = models.TextField()
    fine_category = models.CharField(max_length=100)
    rating = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return f"Outfit of {self.profile.user.username} - {self.id}"


class OutfitPlan(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='plans')
    outfit = models.ForeignKey('UserOutfit', on_delete=models.CASCADE, related_name='plans')
    date = models.DateField()

    note = models.CharField(max_length=120, blank=True)

    class Meta:
        unique_together = ('profile', 'date', 'outfit')
        ordering = ['-date']

    def __str__(self):
        return f"{self.profile.user.username} • {self.date} • {self.outfit_id}"



