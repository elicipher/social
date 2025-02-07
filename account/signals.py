from django.db.models.signals import post_save
from .models import Profile 
from django.contrib.auth.models import User  

def create_profile(sender , **kwargs):
    if kwargs['created']:
        Profile.objects.create(user= kwargs['instance'])

post_save.connect(receiver=create_profile , sender=User)

#post _ save بعد ذخیره سیگنال ارسال میشود
# receiver کسی که سیگنال را دریافت میکند فانکشن بالایی است
# sender کسی که قرار است ارسال کند User است
# این عمل واسه ساخت پروفایل برای کاربران است