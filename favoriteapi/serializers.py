import enum
import datetime
from rest_framework import serializers
from .models import Category, Favorite


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        for key, value in validated_data.items():
            validated_data[key] = value.lower()
        instance, _ = Category.objects.get_or_create(**validated_data)
        return instance


class FavoriteThingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, data):
        metadata = data.get('metadata', None)
        valid_types = [str, int, datetime.date, enum.Enum]
        if metadata:
            for key, value in metadata.items():
                if type(metadata[key]) not in valid_types:
                    raise serializers.ValidationError(
                        'The metadata fields can only contain text, numbers, dates and enumerables'
                    )
        return data
