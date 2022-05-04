from django.urls import path

from authentication.views import UserCreateView

urlpatterns = [
    # path('', VacancyListView.as_view()),
    # path('<int:pk>/', VacancyDetailView.as_view()),
    path('create/', UserCreateView.as_view()),
    # path('<int:pk>/update/', VacancyUpdateView.as_view()),
    # path('<int:pk>/delete/', VacancyDeleteView.as_view()),
    ]





