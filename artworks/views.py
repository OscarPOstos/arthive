from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework.exceptions import PermissionDenied
from .models import Artwork, Layer, Vote
from .serializers import ArtworkSerializer, LayerSerializer, VoteSerializer

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


class ArtworkVoteView(generics.GenericAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """Votar una obra (+1 o -1)"""
        artwork_id = pk
        value = request.data.get("value")

        if value not in [1, -1, "1", "-1"]:
            return Response({"error": "Valor inválido, usa 1 o -1"}, status=400)

        vote, created = Vote.objects.update_or_create(
            artwork_id=artwork_id,
            user=request.user,
            defaults={"value": int(value)}
        )
        return Response(
            {"message": "Voto registrado", "value": vote.value},
            status=status.HTTP_200_OK
        )


class ArtworkVotesCountView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        """Ver conteo de votos"""
        total = Vote.objects.filter(artwork_id=pk).aggregate(score=Sum("value"))["score"] or 0
        likes = Vote.objects.filter(artwork_id=pk, value=1).count()
        dislikes = Vote.objects.filter(artwork_id=pk, value=-1).count()
        return Response({
            "artwork_id": pk,
            "total_score": total,
            "likes": likes,
            "dislikes": dislikes
        })
