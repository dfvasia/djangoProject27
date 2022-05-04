from django.urls import path
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import UserCreateView, Logout

urlpatterns = [
    # path('', VacancyListView.as_view()),
    path('login/', views.obtain_auth_token),
    path('logout/', Logout.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('create/', UserCreateView.as_view()),
    # path('<int:pk>/', VacancyDetailView.as_view()),
    # path('<int:pk>/update/', VacancyUpdateView.as_view()),
    # path('<int:pk>/delete/', VacancyDeleteView.as_view()),
    ]





