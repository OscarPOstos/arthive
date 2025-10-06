from rest_framework import serializers
from .models import Artwork, Layer, Vote, Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "artwork", "user", "content", "created_at"]
        read_only_fields = ["id", "artwork", "user", "created_at"]

class ArtworkSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Artwork
        fields = ["id", "user", "title", "description", "image", "created_at", "is_public"]
        read_only_fields = ["id", "user", "created_at"]

class LayerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Layer
        fields = ["id", "artwork", "user", "image", "created_at"]
        read_only_fields = ["id", "artwork", "user", "created_at"]

class VoteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Vote
        fields = ["id", "artwork", "user", "value", "created_at"]
        read_only_fields = ["id", "artwork", "user", "created_at"]