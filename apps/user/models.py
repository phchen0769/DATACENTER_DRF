from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Router(models.Model):
    """
    路由
    """

    router_id = models.IntegerField(
        default=0,
        primary_key=True,
        verbose_name="路由id",
        help_text="路由id",
    )
    sub_router = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="上级路由",
        help_text="上级路由",
    )
    path = models.CharField(
        null=True, max_length=50, verbose_name="路径", help_text="路径"
    )

    component = models.CharField(
        null=True, max_length=50, verbose_name="组件名称", help_text="组件名称"
    )
    redirect = models.CharField(
        null=True, max_length=30, verbose_name="重定向", help_text="重定向"
    )
    hidden = models.BooleanField(
        default=False, verbose_name="是否隐藏", help_text="是否隐藏"
    )
    name = models.CharField(
        null=True, max_length=30, verbose_name="路由名", help_text="路由名"
    )
    title = models.CharField(
        null=True, max_length=30, verbose_name="路由标题", help_text="路由标题"
    )
    icon = models.CharField(
        null=True, max_length=50, verbose_name="图标", help_text="图标"
    )

    class Meta:
        verbose_name = "路由"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限
    """

    # URL别名
    name = models.CharField(
        null=True, max_length=30, verbose_name="权限名称", help_text="权限名称"
    )
    method = models.CharField(
        null=True, max_length=30, verbose_name="方法类型", help_text="方法类型"
    )
    desc = models.CharField(
        null=True, max_length=300, verbose_name="描述", help_text="描述"
    )
    router = models.ForeignKey(
        Router,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="权限",
        help_text="权限",
    )

    class Meta:
        verbose_name = "权限"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Role(models.Model):
    """
    角色
    """

    name = models.CharField(
        null=True, max_length=30, verbose_name="角色名称", help_text="角色名称"
    )
    desc = models.CharField(
        null=True, max_length=300, verbose_name="描述", help_text="描述"
    )
    permission = models.ManyToManyField(
        Permission,
        verbose_name="权限",
        help_text="权限",
    )

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserProfile(AbstractUser):
    """
    用户
    """

    username = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        unique=True,
        verbose_name="姓名",
        help_text="姓名",
    )
    avatar = models.CharField(
        max_length=200,
        verbose_name="用户头像",
        help_text="用户头像",
        default="https://m.imooc.com/static/wap/static/common/img/logo-small@2x.png",
    )
    birthday = models.DateField(
        null=True, blank=True, verbose_name="生日", help_text="生日"
    )
    address = models.CharField(
        null=True, max_length=50, verbose_name="家庭地址", help_text="家庭地址"
    )
    mobile = models.CharField(max_length=11, verbose_name="手机", help_text="手机")
    gender = models.CharField(
        max_length=6,
        choices=(("male", "男"), ("female", "女")),
        default="female",
        verbose_name="性别",
        help_text="性别",
    )
    email = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="邮箱", help_text="邮箱"
    )

    role = models.ManyToManyField(
        Role,
        verbose_name="角色",
        help_text="角色",
    )

    add_time = models.DateField(
        default=timezone.now,
        verbose_name="添加时间",
        help_text="添加时间",
    )

    def get_routers(self):
        if self.is_anonymous:
            routers = []
            return routers
        else:
            # 获取该用户所有角色
            roles = self.role.all()
            # 获取所有角色的权限
            permissions = Permission.objects.filter(role__in=roles)
            # 获取所有权限的子菜单
            child_routers = Router.objects.filter(permission__in=permissions)
            # 获取所有的上级菜单
            sub_routers = Router.objects.filter(sub_router__isnull=True)
            # 获取所有权限的上级菜单
            routers = sub_routers.filter(
                router_id__in=child_routers.values("sub_router_id")
            )
            # 合并上级菜单和子菜单
            all_routers = routers | child_routers
            return all_routers

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class SmsVerifyCode(models.Model):
    """
    短信验证码
    """

    code = models.CharField(
        null=True, max_length=10, verbose_name="验证码", help_text="验证码"
    )
    mobile = models.CharField(
        null=True, max_length=11, verbose_name="手机", help_text="手机"
    )
    add_time = models.DateTimeField(
        default=timezone.now, verbose_name="添加时间", help_text="添加时间"
    )

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


class EmailVerifyCode(models.Model):
    """
    邮箱验证码
    """

    code = models.CharField(
        null=True, max_length=10, verbose_name="验证码", help_text="验证码"
    )
    email = models.EmailField(
        null=True, unique=True, max_length=100, verbose_name="邮箱", help_text="邮箱"
    )
    add_time = models.DateTimeField(
        default=timezone.now, verbose_name="添加时间", help_text="添加时间"
    )

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
