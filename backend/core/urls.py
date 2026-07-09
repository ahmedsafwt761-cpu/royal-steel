from django.urls import path
from . import views


urlpatterns = [
    path("quotes/", views.QuoteCreateView.as_view(), name="quote-create"),
    path("quotes/list/", views.QuoteListView.as_view(), name="quote-list"),
    path("quotes/<int:pk>/", views.QuoteDetailView.as_view(), name="quote-detail"),
]