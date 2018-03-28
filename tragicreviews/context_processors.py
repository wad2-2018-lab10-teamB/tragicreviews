from tragicreviews.models import Subject

# This is used in the base template to load the categories list for the sidebar,
# rather than have EVERY view pass it in the context dictionary.
def subject_list(request):
	return {"categories": Subject.objects.all()}
