from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.generate_permanent_token import generate_permanent_token
from .models import PermanentToken


class GeneratePermanentTokenView(APIView):
    """
    生成一个长期有效的 Token。
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        token = generate_permanent_token(user)
        return Response(
            {"token": token, "message": "此 Token 永不过期，除非重新生成。"}
        )


class RevokePermanentTokenView(APIView):
    """撤销长期有效的 Token。"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        PermanentToken.objects.filter(user=request.user).delete()
        return Response({"message": "长期 Token 已吊销。"})
