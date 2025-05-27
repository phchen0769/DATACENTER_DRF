from django.db import models

# Create your models here.


class DividendRecord(models.Model):
    """
    工商银行分红记录（来自新浪财经）
    """

    dividend_date = models.DateField(verbose_name="分红公告日期")  # 公告日期
    plan = models.CharField(
        max_length=100, verbose_name="分红方案(每10股)", help_text="分红方案(每10股)"
    )
    status = models.CharField(max_length=20, verbose_name="进度", help_text="分红进度")
    ex_dividend_date = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="除权除息日"
    )
    register_date = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="股权登记日"
    )
    listing_date = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="红股上市日"
    )
    detail = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="查看详细"
    )
    bonus_stock = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="送股(股)"
    )
    transfer_stock = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="转增(股)"
    )
    dividend_amount = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="派息(税前)(元)"
    )

    class Meta:
        verbose_name = "分红记录"
        verbose_name_plural = "分红记录"

    def __str__(self):
        return f"{self.dividend_date} {self.plan} {self.status}"
