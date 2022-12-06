from uuid import uuid4
from django.db import models


class User(models.Model):
    class Meta:
        db_table = "api_users"

    user_id = models.UUIDField(primary_key=True, default=uuid4)

    name = models.CharField(max_length=255)
    image = models.FileField(upload_to="users/", null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


