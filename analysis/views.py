from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import AllowAny
from .utils import perform_analysis
from django.http import JsonResponse, HttpResponse
from rest_framework.authentication import TokenAuthentication
from .utils import generate_chart

@api_view(['POST'])
@permission_classes([AllowAny])
def analyze_data(request):
    data = request.data.get('data')

    if not data:
        return JsonResponse({"error": "Invalid data"}, status=400)

    result = perform_analysis(data)

    return JsonResponse({"result": result})


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([TokenAuthentication])
def chart(request):
    try:
        data = request.data.get('data')
        chart_type = request.data.get('chart_type')

        if not data:
            return JsonResponse({"error": "Invalid data"}, status=400)

        chart_data = generate_chart(data,chart_type)

        response = HttpResponse(chart_data.getvalue(), content_type='image/png')
        response['Content-Disposition'] = 'inline; filename="chart.png"'
        return response

    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
