from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Q, F
from django.http import JsonResponse
from django.views import View
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from DP27.models import Vacancy, Skill
from DP27.serializers import VacancyListSerializer, VacancyDetailSerializer, VacancyCreateSerializer, \
    VacancyUpdateSerializer, SkillSerializer
from DjangoProject27 import settings


class SkillsViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class VacancyListView(ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer

    def get(self, request, *args, **kwargs):
        vacancy_data = request.GET.get('text', None)
        if vacancy_data:
            self.queryset = self.queryset.filter(
                text__icontains=vacancy_data
            )

        skills = request.GET.getlist("skill", None)
        skills_q = None
        for skill in skills:
            if skills_q is None:
                skills_q = Q(skills__name__icontains=skill)
        else:
            skills_q |= Q(skills__name__icontains=skill)

            if skills_q:
                self.queryset = self.queryset.filter(
                    skills_q
                )
        return super().get(request, *args, **kwargs)


class VacancyDetailView(RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer


class VacancyCreateView(CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer


class VacancyUpdateView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)


class VacancyDeleteView(DestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer


class UserVacancyView(View):
    def get(self, request):
        user_qs = User.objects.annotate(vacancies=Count("vacancy"))

        paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = []

        for user in page_obj:
            users.append(
                {
                    "id": user.id,
                    "name": user.username,
                    "vacancies": user.vacancies,
                }
            )

        response = {
            "items": users,
            "num_pages": paginator.num_pages,
            "total": paginator.count,
            "avg": user_qs.aggregate(avg=Avg("vacancies"))["avg"],
        }

        return JsonResponse(response, safe=False)

class VacancylikeView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer

    def put(self, request, *args, **kwargs):
        Vacancy.objects.filter(pk__in=request.data).update(likes=F('likes') + 1)

        return JsonResponse(
            VacancyDetailSerializer(
                Vacancy.objects.filter(pk__in=request.data), many=True
            ).data, safe=False
        )

