from tragicreviews.models import Subject

def subject_list(request):
	return {"categories": Subject.objects.all()}
