from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import CheckInBook

class CheckInBookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CheckInBook
        fields = ['isbn', 'book_id', 'title', 'edition_format', 'edition_id']

