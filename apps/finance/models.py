from django.db import models
from django.utils import timezone

# Create your models here.


class Dividend(models.Model):
    STOCK_TYPE_CHOICES = [
        ("A股", "H股"),
        # Add other types if needed
    ]

    stock_type = models.CharField(
        max_length=10,
        choices=STOCK_TYPE_CHOICES,
        default="A股",
        verbose_name="股票类型",
    )
    stock_code = models.CharField(max_length=20, null=True, verbose_name="股票代码")
    stock_name = models.CharField(max_length=100, null=True, verbose_name="股票名称")
    announcement_date = models.DateField(null=True, blank=True, verbose_name="公告日期")
    ex_dividend_date = models.DateField(
        null=True, blank=True, verbose_name="除权除息日"
    )
    dividend_before_tax = models.CharField(
        "派息(税前)(元)", max_length=32, null=True, blank=True
    )
    payment_date = models.DateField(null=True, blank=True, verbose_name="派息日")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "Dividend"
        verbose_name_plural = "Dividends"

    def __str__(self):
        return f"{self.stock_name}({self.stock_code}) - {self.announcement_date}"
