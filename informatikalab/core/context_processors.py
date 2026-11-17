def global_navigation_context(request):
    user = request.user
    context = {
        'app_name': 'InformatikaLab',
        'is_teacher': False,
        'is_student': False,
        'is_admin': False,
    }
    if user.is_authenticated:
        context['is_teacher'] = getattr(user, 'role', '') == 'teacher'
        context['is_student'] = getattr(user, 'role', '') == 'student'
        context['is_admin'] = getattr(user, 'role', '') == 'admin' or user.is_superuser
    return context
