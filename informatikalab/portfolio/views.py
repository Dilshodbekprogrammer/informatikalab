import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, FileResponse, Http404
from accounts.models import User, ClassRoom
from .models import ProjectSubmission, SubmissionVersion, TeacherFeedback, StudentReflection


@login_required
def portfolio_index_view(request):
    user = request.user
    if user.is_student:
        # O'quvchi o'z portfolio ishlarini ko'radi
        submissions = ProjectSubmission.objects.filter(student=user).select_related(
            'assignment__project_template', 'lesson_step', 'group'
        ).prefetch_related('versions__feedbacks').order_by('-updated_at')

        reflections = StudentReflection.objects.filter(student=user)
        return render(request, 'portfolio/student_portfolio.html', {
            'submissions': submissions,
            'reflections': reflections
        })
    else:
        # O'qituvchi o'z sinflaridagi o'quvchilar ishlarini ko'radi
        if user.is_admin_role:
            submissions = ProjectSubmission.objects.all().select_related(
                'student', 'assignment__classroom', 'assignment__project_template', 'lesson_step'
            ).order_by('-updated_at')
        else:
            submissions = ProjectSubmission.objects.filter(
                assignment__teacher=user
            ).select_related(
                'student', 'assignment__classroom', 'assignment__project_template', 'lesson_step'
            ).order_by('-updated_at')

        return render(request, 'portfolio/teacher_review_list.html', {
            'submissions': submissions
        })


@login_required
def submission_detail_view(request, submission_id):
    user = request.user
    submission = get_object_or_404(
        ProjectSubmission.objects.select_related(
            'student', 'assignment__teacher', 'assignment__classroom', 'lesson_step__project_template', 'group'
        ).prefetch_related('versions__feedbacks__teacher'),
        id=submission_id
    )

    # Kirish huquqi tekshiruvi (IDOR himoyasi)
    if user.is_student:
        # Agar bu individual topshiriq bo'lsa faqat o'zi, agar guruhli bo'lsa o'sha guruh a'zosi
        if submission.student != user and (not submission.group or not submission.group.members.filter(id=user.id).exists()):
            return HttpResponseForbidden("Siz faqat o‘z ishlaringiz yoki o‘z guruhingiz topshiriqlarini ko‘rishingiz mumkin.")
    elif not user.is_admin_role and submission.assignment.teacher != user:
        return HttpResponseForbidden("Siz faqat o‘z sinfingiz o‘quvchilari ishlarini ko‘rishingiz mumkin.")

    versions = submission.versions.all().order_by('-version_number')
    reflection = getattr(submission, 'reflection', None)

    return render(request, 'portfolio/submission_detail.html', {
        'submission': submission,
        'versions': versions,
        'reflection': reflection,
    })


@login_required
def download_submission_file(request, version_id):
    """Bug 2: Faqat ruxsat etilgan foydalanuvchilarga fayl yuklab olish imkoniyati."""
    version = get_object_or_404(SubmissionVersion, id=version_id)
    submission = version.submission
    user = request.user

    if user.is_student:
        is_owner = (submission.student == user)
        is_group_member = (submission.group and submission.group.members.filter(id=user.id).exists())
        if not is_owner and not is_group_member:
            return HttpResponseForbidden("Sizda ushbu faylni yuklab olish huquqi yo‘q.")
    elif not user.is_admin_role and submission.assignment.teacher != user:
        return HttpResponseForbidden("Siz faqat o‘z sinfingiz o‘quvchilari fayllarini yuklab olishingiz mumkin.")

    if not version.attached_file:
        raise Http404("Ushbu versiyaga fayl biriktirilmagan.")

    try:
        file_path = version.attached_file.path
        filename = os.path.basename(file_path)
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
    except (FileNotFoundError, ValueError):
        raise Http404("Fayl diskda topilmadi.")


@login_required
def add_teacher_feedback_view(request, version_id):
    user = request.user
    if not (user.is_teacher or user.is_admin_role):
        return HttpResponseForbidden("Faqat o‘qituvchilar izoh qoldirishi mumkin.")

    version = get_object_or_404(SubmissionVersion, id=version_id)
    submission = version.submission

    if not user.is_admin_role and submission.assignment.teacher != user:
        return HttpResponseForbidden("Siz faqat o‘z sinfingiz o‘quvchisi ishiga izoh bera olasiz.")

    if request.method == 'POST':
        feedback_text = request.POST.get('feedback_text', '').strip()
        requires_revision = request.POST.get('requires_revision') == 'on'
        criteria_clarity = request.POST.get('criteria_clarity', 'A’lo').strip()
        criteria_technical = request.POST.get('criteria_technical', 'To‘g‘ri').strip()
        criteria_creativity = request.POST.get('criteria_creativity', 'Yaxshi').strip()

        if feedback_text:
            TeacherFeedback.objects.create(
                version=version,
                teacher=user,
                feedback_text=feedback_text,
                requires_revision=requires_revision,
                criteria_clarity=criteria_clarity,
                criteria_technical=criteria_technical,
                criteria_creativity=criteria_creativity
            )

            # Bug 4: Faqat eng so'nggi versiyaga fikr bildirilganda asosiy status yangilanadi
            latest_version = submission.versions.order_by('-version_number').first()
            if latest_version and latest_version.id == version.id:
                if requires_revision:
                    submission.status = 'needs_revision'
                    messages.warning(request, f"v{version.version_number} uchun takomillashtirish vazifasi yuborildi.")
                else:
                    submission.status = 'approved'
                    messages.success(request, f"v{version.version_number} muvaffaqiyatli qabul qilindi.")
                submission.save()
            else:
                if requires_revision:
                    messages.warning(request, f"v{version.version_number} uchun izoh saqlandi. (Yangi v{latest_version.version_number} mavjudligi sababli umumiy holat o‘zgartirilmadi).")
                else:
                    messages.info(request, f"v{version.version_number} uchun ijobiy fikr saqlandi. (Yangi v{latest_version.version_number} mavjudligi sababli umumiy holat o‘zgartirilmadi).")

            return redirect('portfolio:submission_detail', submission_id=submission.id)

    return render(request, 'portfolio/add_feedback.html', {
        'version': version,
        'submission': submission
    })


@login_required
def save_reflection_view(request, submission_id):
    user = request.user
    if not user.is_student:
        return HttpResponseForbidden("Faqat o‘quvchilar refleksiya yozishi mumkin.")

    submission = get_object_or_404(ProjectSubmission, id=submission_id)
    if submission.student != user:
        return HttpResponseForbidden("Siz faqat o‘z ishingiz bo‘yicha refleksiya yozishingiz mumkin.")

    if request.method == 'POST':
        what_created = request.POST.get('what_created', '').strip()
        what_error_found = request.POST.get('what_error_found', '').strip()
        how_improved = request.POST.get('how_improved', '').strip()

        if what_created and what_error_found and how_improved:
            reflection, created = StudentReflection.objects.get_or_create(
                submission=submission,
                student=user,
                defaults={
                    'what_created': what_created,
                    'what_error_found': what_error_found,
                    'how_improved': how_improved
                }
            )
            if not created:
                reflection.what_created = what_created
                reflection.what_error_found = what_error_found
                reflection.how_improved = how_improved
                reflection.save()

            messages.success(request, "Yakuniy refleksiya portfoliongizga muvaffaqiyatli saqlandi!")
            return redirect('portfolio:submission_detail', submission_id=submission.id)
        else:
            messages.error(request, "Iltimos, barcha uchta refleksiya savoliga to‘liq javob bering.")

    return redirect('portfolio:submission_detail', submission_id=submission.id)


@login_required
def compare_versions_view(request, submission_id):
    user = request.user
    submission = get_object_or_404(ProjectSubmission, id=submission_id)

    if user.is_student and submission.student != user:
        return HttpResponseForbidden("Ruxsat berilmagan.")
    elif not user.is_admin_role and not user.is_student and submission.assignment.teacher != user:
        return HttpResponseForbidden("Ruxsat berilmagan.")

    v1_id = request.GET.get('v1')
    v2_id = request.GET.get('v2')

    all_versions = submission.versions.all().order_by('version_number')
    if all_versions.count() < 2:
        messages.info(request, "Taqqoslanadigan versiyalar yetarli emas (kamida 2 ta versiya kerak).")
        return redirect('portfolio:submission_detail', submission_id=submission.id)

    version1 = all_versions.filter(version_number=v1_id).first() if v1_id else all_versions.first()
    version2 = all_versions.filter(version_number=v2_id).first() if v2_id else all_versions.last()

    return render(request, 'portfolio/compare_versions.html', {
        'submission': submission,
        'all_versions': all_versions,
        'version1': version1,
        'version2': version2
    })
