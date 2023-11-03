from django.db import models


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False, blank=False)


    class Meta:
        app_label = 'core'