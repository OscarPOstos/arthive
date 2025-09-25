from django.urls import path
from .views import ArtworkListCreateView, ArtworkDetailView, LayerListCreateView

urlpatterns = [
    path("", ArtworkListCreateView.as_view(), name="artwork-list-create"),
    path("<int:pk>/", ArtworkDetailView.as_view(), name="artwork-detail"),
    path("<int:pk>/layers/", LayerListCreateView.as_view(), name="layer-list-create"),
]
