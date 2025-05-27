from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from rest_framework.mixins import CreateModelMixin
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from random import choice
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from datacenter_drf.settings import DEFAULT_FROM_EMAIL

# from rest_framework_bulk import BulkModelViewSet

from rest_framework.decorators import action

from .serializers import (
    SmsSerializer,
    EmailSerializer,
    EmailUserRegSerializer,
    UserDetailSerializer,
    PermissionFieldSerializer,
    PermissionSerializer,
    RoleSerializer,
    RouterSerializer,
    UserInfoSerializer,
)
from datacenter_drf.settings import APIKEY
from utils.yunpian import YunPian


# 导入自定义model
from .models import SmsVerifyCode, EmailVerifyCode, Permission, Role, Router

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            # 重载ModelBackend模块的 authenticate方法，增加了mobile和email登录方式。
            user = User.objects.get(
                Q(username=username) | Q(mobile=username) | Q(email=username)
            )
            # user = UserModel._default_manager.get_by_natural_key(username)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """

    serializer_class = SmsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]

        yun_pian = YunPian(APIKEY)

        # 生成验证码
        code = get_random_string(length=6, allowed_chars="1234567890")

        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status["code"] != 0:
            return Response(
                {"mobile": sms_status["msg"]}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            code_record = SmsVerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({"mobile": mobile}, status=status.HTTP_201_CREATED)


class EmailCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送邮箱验证码
    """

    serializer_class = EmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]

            # 生成验证码
            code = get_random_string(length=4, allowed_chars="1234567890")

            # 创建或更新验证码实例
            EmailVerifyCode.objects.update_or_create(
                email=email, defaults={"code": code, "add_time": timezone.now()}
            )

            # 发送邮件
            send_mail(
                "Your Email Verification Code",
                f"Your verification code is {code}.",
                f"{DEFAULT_FROM_EMAIL}",
                [email],
                fail_silently=False,
            )
            return Response(
                {"message": "Verification code sent successfully!"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserViewSet(
    CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    用户注册、更新、获取用户信息
    """

    serializer_class = EmailUserRegSerializer
    # serializer_class = UserInfoSerializer
    queryset = User.objects.all()
    authentication_classes = (
        JWTAuthentication,
        authentication.SessionAuthentication,
    )

    # get方法的序列化器
    def get_serializer_class(self):
        if self.action == "retrieve" or "get":
            return UserInfoSerializer
        elif self.action == "create":
            return EmailUserRegSerializer

        return UserInfoSerializer

    permission_classes = (permissions.IsAuthenticated,)

    # 重写get_permissions方法，根据不同的action返回不同的权限
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "get":
            # 管理员才可以看到所有用户
            return [permissions.IsAdminUser()]
        elif self.action == "create":
            return []

        return []

    def create(self, request, *args, **kwargs):
        # 取出json数据初始化到serializer中
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 调用serializer保存方法
        user = self.perform_create(serializer)

        # 向前端返回refresh token、access token 以及serializer中的对象
        refresh = RefreshToken.for_user(user)
        re_dict = serializer.data
        re_dict["refresh"] = str(refresh)
        re_dict["access"] = str(refresh.access_token)
        # re_dict["username"] = user.username if user.name else user.username
        re_dict["username"] = user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    # 保存serializer到数据库中
    def perform_create(self, serializer):
        return serializer.save()


class PermissionViewSet(viewsets.ModelViewSet):
    """
    权限
    """

    queryset = Permission.objects.all()
    # serializer_class = PermissionSerializer

    # get方法的序列化器
    def get_serializer_class(self):
        if self.action in ["retrieve", "list"]:
            return PermissionFieldSerializer
        return PermissionSerializer


class RoleViewSet(viewsets.ModelViewSet):
    """
    角色
    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RouterViewSet(viewsets.ModelViewSet):
    """
    路由
    """

    queryset = Router.objects.all()
    serializer_class = RouterSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    用户
    """

    queryset = User.objects.all()
    serializer_class = UserInfoSerializer

    @action(detail=False, methods=["get"])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    # def get_object(self):
    #     return self.request.user


# class UserRoleViewSet(viewsets.ModelViewSet):
#     """
#     用户角色
#     """

#     queryset = User.objects.all()
#     serializer_class = UserRoleSerializer

#     @action(detail=False, methods=["get"])
#     def me(self, request):
#         serializer = self.get_serializer(request.user)
#         return Response(serializer.data)
