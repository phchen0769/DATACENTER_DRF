from rest_framework import serializers
from .models import Dividend


class DividendSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Dividend
        fields = "__all__"
