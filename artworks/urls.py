from django.urls import path
from .views import ArtworkListCreateView, ArtworkDetailView, LayerListCreateView, ArtworkVoteView, ArtworkVotesCountView

urlpatterns = [
    path("", ArtworkListCreateView.as_view(), name="artwork-list-create"),
    path("<int:pk>/", ArtworkDetailView.as_view(), name="artwork-detail"),
    path("<int:pk>/layers/", LayerListCreateView.as_view(), name="layer-list-create"),
    path("<int:pk>/vote/", ArtworkVoteView.as_view(), name="artwork-vote"),
    path("<int:pk>/votes/", ArtworkVotesCountView.as_view(), name="artwork-votes-count"),
]
