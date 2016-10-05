from django.db import models

# Create your models here.
class Lottery(models.Model):
    sn = models.CharField(max_length=8)
    img = models.FileField(null=True,blank=True)
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)
    enabled = models.NullBooleanField(default=False, null=True,blank=True)

    def __str__(self):
        return self.sn +'-used:'+ str(self.enabled)