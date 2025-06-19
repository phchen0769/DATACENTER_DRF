from django.shortcuts import render
from rest_framework import viewsets

from .models import Dividend
from .serializers import DividendSerializer


# Create your views here.
class DividendViewSet(viewsets.ModelViewSet):
    """
    股息记录
    """

    queryset = Dividend.objects.all()
    serializer_class = DividendSerializer
