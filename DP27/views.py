import json

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView

from DP27.models import Vacancy, Skill
from DjangoProject27 import settings


@method_decorator(csrf_exempt, name="dispatch")
class VacancyListView(ListView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        search_text = request.GET.get("text", None)
        if search_text:
            self.object_list = self.object_list(text=search_text)

        self.object_list = self.object_list.order_by("text", "slug")

        # total = self.object_list.count()
        # page_number = int(request.GET.get("page", 1))
        # offset = (page_number-1) * settings.TOTAL_ON_PAGE
        # if (page_number-1) * settings.TOTAL_ON_PAGE < total:
        #     self.object_list = self.object_list[offset:offset+settings.TOTAL_ON_PAGE]
        # else:
        #     self.object_list[offset:offset+total]

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        vacancies = []
        for vacancy in self.object_list:
            vacancies.append({
                "id": vacancy.id,
                "text": vacancy.text,
            })

        response = {
            "items": vacancies,
            "num_pages": paginator.num_pages,
            "total": paginator.count,
        }

        return JsonResponse(response, safe=False)


class VacancyDetailView(DetailView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        vacancy = self.get_object()
        return JsonResponse({
            "id": vacancy.id,
            "slug": vacancy.slug,
            "status": vacancy.status,
            "data": vacancy.data,
            "user": vacancy.user_id,
            })


@method_decorator(csrf_exempt, name='dispatch')
class VacancyCreateView(CreateView):
    model = Vacancy
    fields = ["user", "slug", "text", "status", "created", "skills"]

    def post(self, request, *args, **kwargs):
        vacancy_data = json.loads(request.body)

        vacancy = Vacancy.objects.create(
            user_id=vacancy_data["user_id"],
            slug=vacancy_data["slug"],
            text=vacancy_data["text"],
            status=vacancy_data["status"],

        )

        return JsonResponse({
            "id": vacancy.id,
            "text": vacancy.text
        })


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

