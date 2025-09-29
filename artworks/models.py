from django.db import models
from django.contrib.auth.models import User

class Artwork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="artworks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="artworks/")
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class Layer(models.Model):
    artwork = models.ForeignKey("artworks.Artwork", on_delete=models.CASCADE, related_name="layers")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="layers")
    image = models.ImageField(upload_to="layers/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Layer de {self.user.username} en {self.artwork.title}"

class Vote(models.Model):
    VOTE_CHOICES = [
        (1, "Like"),
        (-1, "Dislike"),
    ]

    artwork = models.ForeignKey("artworks.Artwork", on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="artwork_votes")
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("artwork", "user")  # Un usuario solo puede votar una vez

    def __str__(self):
        return f"{self.user.username} votó {self.value} en {self.artwork.title}"