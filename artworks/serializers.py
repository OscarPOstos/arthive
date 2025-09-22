from rest_framework import serializers
from .models import Artwork

class ArtworkSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Artwork
        fields = ["id", "user", "title", "description", "image", "created_at", "is_public"]
        read_only_fields = ["id", "user", "created_at"]
