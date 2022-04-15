import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from DP27.models import Vacancy


@csrf_exempt
def index(request):
    if request.method == "GET":
        vacancies = Vacancy.objects.all()

        search_text = request.GET.get("text", None)
        if search_text:
            vacancies = vacancies.filter(text=search_text)

        response = []
        for vacancy in vacancies:
            response.append({
                "id": vacancy.id,
                "text": vacancy.text,
            })
        return JsonResponse(response, safe=False)
    elif request.method == "POST":
        vacancy_data = json.loads(request.body)

        vacancy = Vacancy()
        vacancy.text = vacancy_data["text"]

        vacancy.save()
        return JsonResponse({
            "id": vacancy.id,
            "text": vacancy.text
        })


def get(request, vacancy_id):
    if request.method == "GET":
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            return JsonResponse({
                "error": "Not found"
            }, status=404)
        except Vacancy.MultipleObjectsReturned:
            return JsonResponse({
                "error": "Multiple Objects"
            }, status=404)

        return JsonResponse(({
                "id": vacancy.id,
                "text": vacancy.text,
            }), safe=False)

