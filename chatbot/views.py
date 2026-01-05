import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .ai_engine import ai_reply

@csrf_exempt
def chatbot_reply(request):
    if request.method != "POST":
        return JsonResponse({"reply": "Invalid request"}, status=400)

    try:
        data = json.loads(request.body)
        message = data.get("message", "").strip()
    except Exception:
        return JsonResponse({"reply": "Invalid input"})

    if not message:
        return JsonResponse({"reply": "Please type a message."})

    try:
        reply = ai_reply(message)
        return JsonResponse({"reply": reply})
    except Exception as e:
        return JsonResponse({
            "reply": f"AI ERROR: {str(e)}"
        })