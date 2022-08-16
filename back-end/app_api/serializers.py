from rest_framework import serializers
from .models import BankModel
from django.utils.translation import gettext_lazy as _

    
class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankModel
        exclude = ['user']