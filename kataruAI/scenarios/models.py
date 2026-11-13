from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from accounts.models import *
import secrets
# Create your models here.

class Scenario(models.Model):
    class Kind(models.TextChoices):
        CREATE = 'CREATE',  '作成シナリオ'
        NOT_CREATE = 'NOT_CREATE', 'シナリオ'
    class Level(models.TextChoices):
        BEGINNER = 'BEGINNER', '初級'
        INTERMEDIATE = 'INTERMEDIATE', '中級'
        ADVANCED = 'ADVANCED', '上級'
    def create_share_number():
        while True:
            # 8桁のランダムな数字文字列を生成（例: "04829104"）
            code = "".join(secrets.choice("0123456789") for _ in range(8))
            # DBに同じ値が既に存在しないか確認
            if not Scenario.objects.filter(share_code=code).exists():
                return code
    creatoe = models.ForeignKey(
        User,
        verbose_name="作成者",
        on_delete=models.CASCADE
    )
    kind = models.CharField(
        verbose_name="種別(人が作ったか作ってないか)",
        max_length=10,
        choices=Kind.choices,
        default=Kind.NOT_CREATE
    )
    difficulty = models.CharField(
        verbose_name="難易度",
        max_length=12,
        choices=Level.choices,
        default=Level.INTERMEDIATE
    )
    title = models.CharField(
        verbose_name="タイトル",
        max_length=40,
    )
    description = models.CharField(
        verbose_name="説明",
        max_length=10000,
        blank=True,
    )
    # AIで生成させる===============
    character_name = models.CharField(
        verbose_name="キャラクター名",
        max_length=50,
        null=True,
        blank=True
    )
    character_intro = models.TextField(
        verbose_name="キャラクター紹介文(性格)",
        null=True,
        blank=True    )
    goal = models.TextField(
        verbose_name="ゴール条件",
        null=True,
        blank=True    
        )
    condition = models.TextField(
        verbose_name="条件",
        null=True,
        blank=True    
        )
    # ============================
    image = models.TextField( # SVGで生成
        verbose_name="キャラクター画像",
        null=True,
        blank=True
    )
    is_public = models.BooleanField(
        verbose_name="公開シナリオ",
        default=False
    )
    share_code = models.CharField(
        verbose_name="共有コード",
        default=create_share_number,
        max_length=8,
        unique=True,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        verbose_name="作成日時",
        auto_now_add=True
    )
    update_at = models.DateTimeField(
        verbose_name="更新日時",
        auto_now_add=True
    )
    delete_at = models.DateTimeField(
        verbose_name="削除日時",
        auto_now_add=True
    )
