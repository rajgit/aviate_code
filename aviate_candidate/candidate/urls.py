from django.urls import path

from .views import CandidateSearchView

urlpatterns = [
    path('search/', CandidateSearchView.as_view(), name='search'),
]
