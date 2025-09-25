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