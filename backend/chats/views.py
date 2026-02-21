from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from model.response import generate_reply

def test(request):
    return HttpResponse("Rem Backend Server is running")

@csrf_exempt
def chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message", "")
        reply = generate_reply(message)
        return JsonResponse({"reply": reply})