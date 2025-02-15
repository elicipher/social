from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Relation(models.Model):
    from_user = models.ForeignKey(User , on_delete=models.CASCADE , related_name= 'followers')
    to_user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='following')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} following {self.to_user}'

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    img_user = models.ImageField(upload_to='profiles/',null=True , blank=True)
    banner = models.ImageField(upload_to='banner/',null=True , blank=True)
    age = models.PositiveBigIntegerField(default=0)
    bio = models.TextField(null = True ,blank =True)

