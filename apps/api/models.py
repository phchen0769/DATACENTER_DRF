from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.


class PermanentToken(models.Model):
    """
    长期有效的 Token 模型，存储在数据库中。
    - 用户手动生成后，Token 永不过期（除非用户重新生成或删除）。
    - 每次生成新 Token 时，旧 Token 会被自动删除。
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="permanent_tokens",  # 反向查询名称
    )
    key = models.CharField(max_length=64, unique=True, help_text="随机生成的 Token 值")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="Token 创建时间")
    last_used = models.DateTimeField(
        null=True, blank=True, help_text="最后一次使用时间"
    )

    def __str__(self):
        return f"Permanent Token for {self.user.username}"

    class Meta:
        verbose_name = "长期 Token"
        verbose_name_plural = "长期 Token"
        ordering = ["-add_time"]  # 按创建时间倒序排列
