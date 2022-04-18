import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView

from DP27.models import Vacancy, Skill


@method_decorator(csrf_exempt, name="dispatch")
class VacancyListView(ListView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        search_text = request.GET.get("text", None)
        if search_text:
            self.object_list = self.object_list(text=search_text)

        response = []
        for vacancy in self.object_list:
            response.append({
                "id": vacancy.id,
                "text": vacancy.text,
            })
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
