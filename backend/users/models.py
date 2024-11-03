import uuid

from django.db import models


""" Models for domain Users

Create your Database Tables here. Schemas are defined in schemas.py
"""


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nickname = models.CharField(max_length=100)
