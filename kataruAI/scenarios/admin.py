from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ("creatoe", "kind", "difficulty", "title", "description", "character_name", "character_intro", "goal", "condition", "is_public", "share_code", "created_at")
    search_fields = ("creatoe",)