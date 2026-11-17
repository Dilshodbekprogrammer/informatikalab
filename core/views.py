from django.shortcuts import render
from methods.models import TeachingMethod
from lessons.models import LessonPlan
from projects.models import ClassProjectAssignment, ProjectTemplate
from portfolio.models import ProjectSubmission


def home_view(request):
    user = request.user
    methods = TeachingMethod.objects.filter(is_active=True).order_by('order')[:5]
    featured_project = ProjectTemplate.objects.filter(is_active=True).first()

    context = {
        'methods': methods,
        'featured_project': featured_project,
    }

    if user.is_authenticated:
        if user.is_teacher or user.is_admin_role:
            # O'qituvchi statistikasi
            my_lessons = LessonPlan.objects.filter(teacher=user) if not user.is_admin_role else LessonPlan.objects.all()
            pending_reviews = ProjectSubmission.objects.filter(
                assignment__teacher=user,
                status__in=['submitted', 'resubmitted']
            ) if not user.is_admin_role else ProjectSubmission.objects.filter(status__in=['submitted', 'resubmitted'])

            context.update({
                'my_lessons_count': my_lessons.count(),
                'pending_reviews_count': pending_reviews.count(),
                'recent_lessons': my_lessons[:4],
                'pending_submissions': pending_reviews[:5],
            })
        else:
            # O'quvchi statistikasi
            enrolled_classes = user.enrolled_classes.all()
            assigned_lessons = LessonPlan.objects.filter(
                classroom__in=enrolled_classes,
                status='assigned'
            )
            my_submissions = ProjectSubmission.objects.filter(student=user).select_related('lesson_step')
            needs_revision_submissions = my_submissions.filter(status='needs_revision')

            context.update({
                'assigned_lessons': assigned_lessons[:4],
                'my_submissions': my_submissions[:4],
                'needs_revision_submissions': needs_revision_submissions,
            })

    return render(request, 'core/home.html', context)
