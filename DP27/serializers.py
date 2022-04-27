
from rest_framework import serializers

from DP27.models import Vacancy


class VacancyListSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Vacancy
        fields = ["id", "text", "slug", "status", "data", "user", "skills"]


class VacancyDetailSerializer(serializers.ModelSerializer):
    # user = serializers.CharField()

    class Meta:
        model = Vacancy
        fields = '__all__'
