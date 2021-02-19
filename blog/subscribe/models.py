from django.db import models


class SubscribeModel(models.Model):
    sys_id = models.AutoField(primary_key=True, null=False, blank=True)
    email = models.EmailField(null=False, blank=True, max_length=200, unique=True)
    created_date = models.DateTimeField(null=False, blank=True)

    def __str__(self):
        return self.email
