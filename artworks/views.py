from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Artwork, Layer
from .serializers import ArtworkSerializer, LayerSerializer

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

class LayerListCreateView(generics.ListCreateAPIView):
    serializer_class = LayerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        artwork_id = self.kwargs["pk"]
        return Layer.objects.filter(artwork_id=artwork_id).order_by("created_at")

    def perform_create(self, serializer):
        artwork_id = self.kwargs["pk"]
        serializer.save(user=self.request.user, artwork_id=artwork_id)
