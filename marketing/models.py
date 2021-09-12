from django.db import models

# Create your models here.
class SignUp(models.Model):
    email = models.EmailField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email 