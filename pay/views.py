from django.http import JsonResponse
import requests
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([TokenAuthentication])
def make_payment(request):
    amount = request.data.get('amount')
    currency = request.data.get('currency')
    from_phone = request.data.get('from')
    description = request.data.get('description')
    external_reference = request.data.get('external_reference')
    external_user = request.data.get('external_user')

    if not all([amount, currency, from_phone, description]):
        return JsonResponse({"error": "Invalid payment request data"}, status=400)


    campay_api_url = 'https://demo.campay.net/api/collect/'
    campay_request_data = {
        "amount": amount,
        "currency": currency,
        "from": from_phone,
        "description": description,
        "external_reference": external_reference,
        "external_user": external_user
    }

    try:
        response = requests.post(campay_api_url, json=campay_request_data, headers={
            'Authorization': 'Token YOUR_CAMPAY_API_TOKEN',
            'Content-Type': 'application/json'
        })

        if not response.ok:
            raise Exception(f"Campay API error: {response.status_code}")

        campay_response_data = response.json()


        return JsonResponse(campay_response_data, status=200)

    except Exception as e:
        print(f"Error making Campay API request: {e}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)
