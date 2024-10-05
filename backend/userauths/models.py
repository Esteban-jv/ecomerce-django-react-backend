from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from shortuuid.django_fields import ShortUUIDField

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    phone = models.CharField(max_length=18, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name','phone']
    def get_image(self):
        return self.image.url if self.image else None
    def __str__(self):
        return f'{self.email}: {self.first_name}'

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split("@")[0]
        super().save(*args, **kwargs)

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet='abcdefghijk1235')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField('profile_picture', upload_to='users/profile', max_length=255, null=True, blank=False)
    about = models.TextField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=30, null=True, blank=False)
    country = models.CharField(max_length=100, null=True, blank=False)
    city = models.CharField(max_length=150, null=True, blank=False)
    state = models.CharField(max_length=100, null=True, blank=False)
    address = models.CharField(max_length=255, null=True, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email}: {self.user.first_name}'


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)