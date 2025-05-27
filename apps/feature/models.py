from django.db import models
from django.utils import timezone


# Create your models here.
class Feature(models.Model):
    title = models.CharField(
        null=True, max_length=40, verbose_name="标题", help_text="标题"
    )
    percentage = models.IntegerField(default=0, verbose_name="进度", help_text="进度")
    content = models.CharField(
        null=True, max_length=2000, verbose_name="内容", help_text="内容"
    )
    add_time = models.DateTimeField(default=timezone.now, verbose_name="发布时间")

    class Meta:
        app_label = "feature"
        verbose_name = "功能"
        verbose_name_plural = "功能"

    def __str__(self):
        return self.title
