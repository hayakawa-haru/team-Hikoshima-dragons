from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid

# Create your models here.
class User(AbstractBaseUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4
    )

    username = models.CharField(
        max_length=20,
        unique=False,
        default="テストユーザー"
    )

    email = models.EmailField(
        unique=True,
    )

    # パスワードはデフォルトで設定されてるため書かない

    create_at = models.DateTimeField(
        auto_now_add=True,
    )

    update_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )

    deleted_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=False
    )

class UserSetting(models.Model):
    user = models.ForeignKey(
        User,
        primary_key=True,
        on_delete=models.CASCADE
    )