# serializers.py
from rest_framework import serializers
from searchbar.models import data
from .models import Feedback

class SourceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = data
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
