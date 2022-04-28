import json

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from rest_framework.generics import ListAPIView

from DP27.models import Vacancy, Skill
from DP27.serializers import VacancyListSerializer, VacancyDetailSerializer, VacancyCreateSerializer
from DjangoProject27 import settings


@method_decorator(csrf_exempt, name="dispatch")
class VacancyListView(ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer

    # def get(self, request, *args, **kwargs):
    #     super().get(request, *args, **kwargs)

        # search_text = request.GET.get("text", None)
        # if search_text:
        #     self.object_list = self.object_list(text=search_text)
        #
        # paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        # page_number = request.GET.get("page")
        # page_obj = paginator.get_page(page_number)
        #
        # list(map(lambda x: setattr(x, "username", x.user.username if x.user else None), page_obj))
        #
        # response = {
        #     "items": VacancyListSerializer(page_obj, many=True).data,
        #     "num_pages": paginator.num_pages,
        #     "total": paginator.count,
        # }
        #
        # return JsonResponse(response, safe=False)


class VacancyDetailView(DetailView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        vacancy = self.get_object()
        return JsonResponse(VacancyDetailSerializer(vacancy).data)


@method_decorator(csrf_exempt, name='dispatch')
class VacancyCreateView(CreateView):
    model = Vacancy
    fields = ["user", "slug", "text", "status", "created", "skills"]

    def post(self, request, *args, **kwargs):
        vacancy_data = VacancyCreateSerializer(data=json.loads(request.body))
        if vacancy_data.is_valid():
            vacancy_data.save()
        else:
            return JsonResponse(vacancy_data.errors)

        return JsonResponse(vacancy_data.data)


@method_decorator(csrf_exempt, name='dispatch')
class VacancyUpdateView(UpdateView):
    model = Vacancy
    fields = ["slug", "text", "status", "skills"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        vacancy_data = json.loads(request.body)
        self.object.slug = vacancy_data["slug"]
        self.object.text = vacancy_data["text"]
        self.object.status = vacancy_data["status"]

        for skill in vacancy_data["skills"]:
            try:
                skill_obj = Skill.objects.get(name=skill)
            except Skill.DoesNotExist:
                return JsonResponse(
                    {
                        "error": "Skill not found"
                    }, status=404
                )
            self.object.skills.add(skill_obj)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "slug": self.object.slug,
            "status": self.object.status,
            "data": self.object.data,
            "user": self.object.user_id,
            "skill": list(self.object.all().values_list("name", flat=True)),
        })


@method_decorator(csrf_exempt, name='dispatch')
class VacancyDeleteView(DeleteView):
    model = Vacancy
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "OK"}, status=200)


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

