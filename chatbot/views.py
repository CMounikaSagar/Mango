from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
import json

# Simple rule-based response logic
def get_bot_response(message):
    message = message.lower()

    if "price" in message:
        return "Our mangoes start at ₹100 per kg."
    elif "types" in message or "varieties" in message:
        return "We sell Alphonso, Banganapalli, and Dasheri mangoes."
    elif "delivery" in message:
        return "Yes, we offer home delivery across India."
    elif "bulk" in message:
        return "For bulk orders, please contact us via email or WhatsApp."
    elif "hello" in message or "hi" in message:
        return "Hi there! How can I help you with mangoes today?"
    else:
        return "Sorry, I didn’t understand that. Can you ask in a different way?"

# Load chatbot page
def chatbot_ui(request):
    return render(request, 'chatbot/index.html')

# Handle AJAX POST requests
@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')
        reply = get_bot_response(user_message)
        return JsonResponse({'reply': reply})
