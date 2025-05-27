# -*- coding: utf-8 -*-
import json
import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime
from datetime import timedelta
from rest_framework.validators import UniqueValidator

# 处理大量数据时使用
# from rest_framework_bulk import BulkSerializerMixin

from .models import SmsVerifyCode, EmailVerifyCode, Role, Permission, Router

from datacenter_drf.settings import REGEX_MOBILE, REGEX_EMAIL, TIME_ZONE

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    """
    短信序列化器
    """

    mobile = serializers.CharField(max_length=11)

    # 验证手机号码
    def validate_mobile(self, mobile):
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if SmsVerifyCode.objects.filter(
            add_time__gt=one_mintes_ago, mobile=mobile
        ).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile


class EmailSerializer(serializers.Serializer):
    """
    邮箱序列化器
    """

    email = serializers.EmailField()

    # 验证邮箱
    def validate_email(self, email):
        # 邮箱是否注册
        if User.objects.filter(email=email).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证邮箱是否合法
        if not re.match(REGEX_EMAIL, email):
            raise serializers.ValidationError("邮箱号码非法")

        return email


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """

    class Meta:
        model = User
        fields = ("username", "gender", "birthday", "email", "mobile")


class UserRegSerializer(serializers.ModelSerializer):
    """
    短信注册
    """

    code = serializers.CharField(
        required=True,
        write_only=True,
        max_length=4,
        min_length=4,
        label="验证码",
        error_messages={
            "blank": "请输入验证码",
            "required": "请输入验证码",
            "max_length": "验证码格式错误",
            "min_length": "验证码格式错误",
        },
        help_text="验证码",
    )
    username = serializers.CharField(
        label="用户名",
        help_text="用户名",
        required=True,
        allow_blank=False,
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="用户已经存在")
        ],
    )

    password = serializers.CharField(
        style={"input_type": "password"},
        help_text="密码",
        label="密码",
        write_only=True,
    )

    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate_code(self, code):
        # try:
        #     verify_records = VerifyCode.objects.get(mobile=self.initial_data["username"], code=code)
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass
        verify_records = SmsVerifyCode.objects.filter(
            mobile=self.initial_data["username"]
        ).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]

            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")


class EmailUserRegSerializer(serializers.ModelSerializer):
    """
    邮箱注册
    """

    code = serializers.CharField(
        required=True,
        write_only=True,
        max_length=4,
        min_length=4,
        label="验证码",
        error_messages={
            "blank": "请输入验证码",
            "required": "请输入验证码",
            "max_length": "验证码格式错误",
            "min_length": "验证码格式错误",
        },
        help_text="验证码",
    )
    username = serializers.CharField(
        label="用户名",
        help_text="用户名",
        required=True,
        allow_blank=False,
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="用户已经存在")
        ],
    )

    password = serializers.CharField(
        style={"input_type": "password"},
        help_text="密码",
        label="密码",
        write_only=True,
    )

    # 校验验证码
    def validate_code(self, code):
        # try:
        #     verify_records = VerifyCode.objects.get(mobile=self.initial_data["username"], code=code)
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass

        # 取出最新的记录
        verify_records = EmailVerifyCode.objects.filter(
            # email=self.initial_data["username"]
            email=self.initial_data["email"]
        ).order_by("-add_time")

        if verify_records:
            last_record = verify_records[0]

            one_hour_ago = datetime.now() - timedelta(hours=1, minutes=0, seconds=0)
            if one_hour_ago > last_record.add_time.replace(tzinfo=None):
                raise serializers.ValidationError(f"验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        # attrs["email"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "email", "password")


# 为角色信息提供name字段(多对多)
class PermissionField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "id": value.id,
            "name": value.name,
            "method": value.method,
            "desc": value.desc,
            "router": value.router_id,
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict) or "id" not in data:
            raise serializers.ValidationError("Invalid format for role data")
        return Permission.objects.get(id=data["id"])


class RoleSerializer(serializers.ModelSerializer):
    """
    角色-权限序列化类
    """

    # 获取用户角色id
    permission = PermissionField(many=True, queryset=Role.objects.all())

    class Meta:
        model = Role
        fields = "id", "name", "desc", "permission"

    # 重写update方法，处理role多对多关系
    def update(self, instance, validated_data):
        # 使用父类的update方法处理其他字段
        instance = super().update(instance, validated_data)

        # 更新permission字段
        permissions_data = set(validated_data.pop("permission", []))

        current_permissions = set(instance.permission.all())

        # 找出需要删除的角色
        permissions_to_remove = current_permissions - permissions_data

        # 删除需要删除的角色
        for permission in permissions_to_remove:
            instance.permission.remove(permission)

        # 添加新的角色
        for permission in permissions_data:
            instance.permission.add(permission)

        return instance


# class RoleSerializer(serializers.ModelSerializer):
#     """
#     普通角色序列化类
#     """

#     class Meta:
#         model = Role
#         fields = "__all__"


# class GroupSerializer(serializers.ModelSerializer):
#     """
#     组序列化类
#     """

#     class Meta:
#         model = Group
#         fields = "__all__"


class RouterSerializer(serializers.ModelSerializer):
    """
    路由序列化类
    """

    class Meta:
        model = Router
        fields = "__all__"


class PermissionSerializer(serializers.ModelSerializer):
    """
    权限序列化类
    """

    class Meta:
        model = Permission
        fields = "__all__"


class PermissionFieldSerializer(serializers.ModelSerializer):
    """
    权限字段序列化类
    """

    # 权限路由
    router = RouterSerializer()

    class Meta:
        model = Permission
        fields = (
            "id",
            "name",
            "method",
            "desc",
            "router",
        )


# 为用户信息提供name字段(多对多)
class RoleField(serializers.RelatedField):
    def to_representation(self, value):
        return {"id": value.id, "name": value.name}

    def to_internal_value(self, data):
        if not isinstance(data, dict) or "id" not in data:
            raise serializers.ValidationError("Invalid format for role data")
        return Role.objects.get(id=data["id"])


class UserInfoSerializer(serializers.ModelSerializer):
    """
    用户信息序列化类
    """

    # 获取用户角色id
    role = RoleField(many=True, queryset=Role.objects.all())

    # 获取用户路由
    routers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "mobile",
            "avatar",
            "address",
            "routers",
            "role",
            "add_time",
        )

    # 获取用户的菜单
    def get_routers(self, obj):
        # 获取用户的菜单并去重
        routers = obj.get_routers().distinct()
        return RouterSerializer(routers, many=True).data

    # 重写update方法，处理role多对多关系
    def update(self, instance, validated_data):
        # 使用父类的update方法处理其他字段
        instance = super().update(instance, validated_data)

        # 更新role字段
        roles_data = set(validated_data.pop("role", []))

        current_roles = set(instance.role.all())

        # 找出需要删除的角色
        roles_to_remove = current_roles - roles_data

        # 删除需要删除的角色
        for role in roles_to_remove:
            instance.role.remove(role)

        # 添加新的角色
        for role in roles_data:
            instance.role.add(role)

        return instance


# class UserRoleSerializer(serializers.ModelSerializer):
#     """
#     用户角色序列化类
#     """

#     class Meta:
#         model = User
#         fields = ("id", "role")
