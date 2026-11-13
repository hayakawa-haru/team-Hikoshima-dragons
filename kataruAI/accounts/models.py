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
        verbose_name="名前",
        max_length=20,
        unique=False,
        default="テストユーザー"
    )

    email = models.EmailField(
        verbose_name="メールアドレス",
        unique=True,
    )

    # パスワードはデフォルトで設定されてるため書かない

    create_at = models.DateTimeField(
        verbose_name="アカウント作成日",
        auto_now_add=True,
    )

    update_at = models.DateTimeField(
        verbose_name="アカウント更新日",
        auto_now_add=True,
        null=True,
        blank=True
    )

    deleted_at = models.DateTimeField(
        verbose_name="アカウント削除日",
        auto_now_add=True,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        "アカウントが削除されてるか",
        default=False
    )

class UserSetting(models.Model):
    user = models.ForeignKey(
        User,
        primary_key=True,
        on_delete=models.CASCADE
    )