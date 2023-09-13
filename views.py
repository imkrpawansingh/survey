# survey_app/views.py

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Survey, Question, Response as SurveyResponse
from .serializers import SurveySerializer, QuestionSerializer, ResponseSerializer
from django.db.models import Count, F, ExpressionWrapper, FloatField
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ResponseViewSet(viewsets.ModelViewSet):
    queryset = SurveyResponse.objects.all()
    serializer_class = ResponseSerializer

    @action(detail=False, methods=['GET'])
    def similarity(self, request):
        # Implement similarity calculation logic here
        # Return similarity results as JSON response
        pass


# survey_app/views.py

# from django.db.models import Count, F, ExpressionWrapper, FloatField
# from django.db.models.functions import Coalesce
# from django.http import JsonResponse

@action(detail=False, methods=['GET'])
def similarity(self, request):
    candidate_id = request.GET.get('candidate_id')
    candidates = Response.objects.values('candidate_name').distinct()

    if candidate_id:
        candidates = candidates.filter(candidate_name__icontains=candidate_id)

    similarity_results = []

    for candidate in candidates:
        candidate_name = candidate['candidate_name']
        candidate_responses = Response.objects.filter(candidate_name=candidate_name)
        total_similarity = 0
        num_comparisons = 0

        for other_candidate in candidates:
            other_candidate_name = other_candidate['candidate_name']
            other_candidate_responses = Response.objects.filter(candidate_name=other_candidate_name)
            common_questions = candidate_responses.filter(question__in=other_candidate_responses.values('question'))

            if common_questions.exists():
                candidate_options = common_questions.values('selected_option')
                other_candidate_options = other_candidate_responses.filter(question__in=common_questions.values('question')).values('selected_option')

                # Calculate Jaccard similarity
                intersection_count = candidate_options.filter(selected_option__in=other_candidate_options).count()
                union_count = candidate_options.union(other_candidate_options).count()

                similarity = intersection_count / union_count
                total_similarity += similarity
                num_comparisons += 1

        if num_comparisons > 0:
            average_similarity = total_similarity / num_comparisons
            similarity_results.append({
                'candidate_name': candidate_name,
                'similarity_percentage': average_similarity * 100
            })

    return JsonResponse({'results': similarity_results})

# survey_app/views.py

# from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 5  # Number of results per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class ResponseViewSet(viewsets.ModelViewSet):
    # ...

    pagination_class = CustomPagination  # Enable pagination using the CustomPagination class


# Create your views here.
