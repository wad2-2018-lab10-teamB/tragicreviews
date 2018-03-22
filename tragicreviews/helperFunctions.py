def getUserDetails(UserProfile):

    user_dictionary = {
        'user': UserProfile.user,
        'image': UserProfile.image if bool(UserProfile.image) else False,
        'levels': UserProfile.level,
        'majors': UserProfile.majors.all(),
    }

    return user_dictionary
