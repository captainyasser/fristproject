
        # ranks/serializers.py
from rest_framework import serializers
from .models import Rank

class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = ['id', 'name']


