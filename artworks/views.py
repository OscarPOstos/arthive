from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Artwork
from .serializers import ArtworkSerializer

# GET /api/artworks/  |  POST /api/artworks/
class ArtworkListCreateView(generics.ListCreateAPIView):
    queryset = Artwork.objects.filter(is_public=True).order_by("-created_at")
    serializer_class = ArtworkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# GET /api/artworks/{id}/  |  DELETE /api/artworks/{id}/
class ArtworkDetailView(generics.RetrieveDestroyAPIView):
    queryset = Artwork.objects.filter(is_public=True)
    serializer_class = ArtworkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("No puedes eliminar obras de otros usuarios.")
        instance.delete()
