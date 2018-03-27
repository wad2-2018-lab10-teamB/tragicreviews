import json
from django.http import JsonResponse, HttpResponseBadRequest
from haystack.query import SearchQuerySet

def search_autocomplete(request):
	search_query = request.GET.get("q", None)
	if not search_query:
		return HttpResponseBadRequest()
	return JsonResponse({
		"results": [str(result.object) for result in SearchQuerySet().autocomplete(autocomplete=search_query)[:5]]
	})
