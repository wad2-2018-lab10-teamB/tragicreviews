from tragicreviews.models import Subject

def base_bootstrap():
    context_dict = {'categories': []}

    subjects = Subject.objects.all()

    for subject in subjects:
        context_dict['categories'].append(subject)

    return (context_dict)

def getUserDetails(UserProfile):

    user_dictionary = {
        'user': UserProfile.user,
        'image': UserProfile.image if bool(UserProfile.image) else False,
        'levels': UserProfile.level,
        'majors': UserProfile.majors.all(),
    }

    return user_dictionary