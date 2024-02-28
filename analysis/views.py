from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework.authentication import TokenAuthentication
from .utils import perform_analysis, generate_chart, table2json

@api_view(['POST'])
@permission_classes([AllowAny])
def analyze_data(request):
    try:
        data = request.data.get('data')

        if not data:
            return JsonResponse({"error": "Invalid data"}, status=400)

        result = perform_analysis(data)

        return JsonResponse({"result": result})

    except Exception as e:
        return JsonResponse({"error": f"An error occurred during analysis: {str(e)}"}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def chart(request):
    try:
        data = request.data.get('data')
        chart_type = request.data.get('chart_type')

        if not data:
            return JsonResponse({"error": "Invalid data"}, status=400)

        chart_data = generate_chart(data, chart_type)

        response = HttpResponse(chart_data.getvalue(), content_type='image/png')
        response['Content-Disposition'] = 'inline; filename="chart.png"'
        return response

    except Exception as e:
        return JsonResponse({"error": f"An error occurred during chart generation: {str(e)}"}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def form(request):
    try:
        data = request.data.get('file')
        if not data:
            return JsonResponse({"error": "Invalid data"}, status=400)
        form = table2json(data)
        return Response(form)

    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
