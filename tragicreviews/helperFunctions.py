from tragicreviews.models import Subject

def base_bootstrap():
    context_dict = {'categories': []}

    subjects = Subject.objects.all()

    for subject in subjects:
        context_dict['categories'].append(subject)

    return (context_dict)
