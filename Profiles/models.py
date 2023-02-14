from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    screen_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now_add=True)
    profile_image = models.ImageField(
        upload_to='images/', default='../default_profile_o66zvl'
    )

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.author}'s profile"


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(author=instance)

# every time a user is created the signal will trigger the profile module to be created
post_save.connect(create_profile, sender=User)