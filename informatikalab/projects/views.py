import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils import timezone
from accounts.models import ClassRoom, User
from labs.models import LabExperimentSubmission
from portfolio.models import ProjectSubmission, SubmissionVersion
from .models import ProjectTemplate, ProjectLessonStep, ClassProjectAssignment, ProjectGroup


@login_required
def projects_index_view(request):
    user = request.user
    templates = ProjectTemplate.objects.filter(is_active=True).prefetch_related('steps')

    if user.is_teacher or user.is_admin_role:
        if user.is_admin_role:
            assignments = ClassProjectAssignment.objects.all().select_related('classroom', 'project_template', 'teacher')
        else:
            assignments = ClassProjectAssignment.objects.filter(teacher=user).select_related('classroom', 'project_template')
    else:
        # O'quvchiga uning sinfi darslari
        enrolled_classes = user.enrolled_classes.all()
        assignments = ClassProjectAssignment.objects.filter(classroom__in=enrolled_classes).select_related('classroom', 'project_template', 'teacher')

    return render(request, 'projects/index.html', {
        'templates': templates,
        'assignments': assignments
    })


@login_required
def project_detail_view(request, project_id):
    user = request.user
    project = get_object_or_404(ProjectTemplate, id=project_id, is_active=True)
    steps = project.steps.all().order_by('lesson_number')

    # O'quvchi uchun topshirilgan ishlarni ko'rish
    user_submissions = {}
    if user.is_student:
        submissions = ProjectSubmission.objects.filter(student=user, lesson_step__project_template=project).select_related('lesson_step')
        for sub in submissions:
            user_submissions[sub.lesson_step.id] = sub

    return render(request, 'projects/detail.html', {
        'project': project,
        'steps': steps,
        'user_submissions': user_submissions,
    })


@login_required
def assign_project_view(request, project_id):
    user = request.user
    if not (user.is_teacher or user.is_admin_role):
        return HttpResponseForbidden("Faqat o‘qituvchilar loyihani sinfga biriktirishi mumkin.")

    project = get_object_or_404(ProjectTemplate, id=project_id)
    classrooms = ClassRoom.objects.filter(teacher=user) if not user.is_admin_role else ClassRoom.objects.all()

    if request.method == 'POST':
        classroom_id = request.POST.get('classroom_id')
        is_group_project = request.POST.get('is_group_project') == 'on'
        deadline = request.POST.get('deadline') or None

        classroom = get_object_or_404(ClassRoom, id=classroom_id)
        if not user.is_admin_role and classroom.teacher != user:
            return HttpResponseForbidden("Siz faqat o‘zingizga biriktirilgan sinfga loyiha biriktira olasiz.")

        assignment = ClassProjectAssignment.objects.create(
            project_template=project,
            classroom=classroom,
            teacher=user,
            is_group_project=is_group_project,
            deadline=deadline
        )

        messages.success(request, f"'{project.title}' loyihasi {classroom.name} sinfiga biriktirildi.")
        return redirect('projects:assignment_detail', assignment_id=assignment.id)

    return render(request, 'projects/assign.html', {
        'project': project,
        'classrooms': classrooms
    })


@login_required
def assignment_detail_view(request, assignment_id):
    user = request.user
    assignment = get_object_or_404(ClassProjectAssignment, id=assignment_id)

    # Kirish huquqi: o'qituvchi o'z biriktirmasini, o'quvchi faqat o'z sinfiga tegishli biriktirmani ko'ra oladi
    if user.is_student:
        if not assignment.classroom.students.filter(id=user.id).exists():
            return HttpResponseForbidden("Sizda bu loyihani ko‘rish huquqi yo‘q (boshqa sinf).")
    elif not user.is_admin_role and assignment.teacher != user:
        return HttpResponseForbidden("Siz faqat o‘z sinflaringiz loyihalarini boshqarishingiz mumkin.")

    steps = assignment.project_template.steps.all().order_by('lesson_number')
    groups = assignment.groups.prefetch_related('members', 'leader')

    # O'quvchi uchun topshirilgan ishlar xaritasi
    student_submissions = {}
    if user.is_student:
        subs = ProjectSubmission.objects.filter(assignment=assignment, student=user)
        for s in subs:
            student_submissions[s.lesson_step.id] = s

    return render(request, 'projects/assignment_detail.html', {
        'assignment': assignment,
        'steps': steps,
        'groups': groups,
        'student_submissions': student_submissions,
    })


@login_required
def group_create_view(request, assignment_id):
    user = request.user
    assignment = get_object_or_404(ClassProjectAssignment, id=assignment_id)
    if not user.is_admin_role and assignment.teacher != user:
        return HttpResponseForbidden("Faqat mas'ul o‘qituvchi guruhlarni shakllantirishi mumkin.")

    class_students = assignment.classroom.students.all()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        leader_id = request.POST.get('leader_id')
        member_ids = request.POST.getlist('members[]')
        role_distribution = request.POST.get('role_distribution', '').strip()

        if name and leader_id:
            leader = get_object_or_404(User, id=leader_id)
            group = ProjectGroup.objects.create(
                assignment=assignment,
                name=name,
                leader=leader,
                role_distribution=role_distribution
            )
            group.members.set(member_ids)
            group.members.add(leader)
            messages.success(request, f"'{name}' guruhi muvaffaqiyatli tuzildi.")
            return redirect('projects:assignment_detail', assignment_id=assignment.id)

    return render(request, 'projects/group_create.html', {
        'assignment': assignment,
        'class_students': class_students
    })


@login_required
def submit_lesson_step_view(request, assignment_id, step_id):
    user = request.user
    assignment = get_object_or_404(ClassProjectAssignment, id=assignment_id)
    step = get_object_or_404(ProjectLessonStep, id=step_id, project_template=assignment.project_template)

    if not user.is_student:
        return HttpResponseForbidden("Faqat o‘quvchilar loyiha topshiriqlarini topshirishi mumkin.")

    # Sinfga a'zolik tekshiruvi (boshqa o'quvchi topshira olmaydi)
    if not assignment.classroom.students.filter(id=user.id).exists():
        return HttpResponseForbidden("Siz faqat o‘z sinfingiz topshiriqlarini yubora olasiz.")

    # Mavjud submission yoki yangi
    submission, created = ProjectSubmission.objects.get_or_create(
        assignment=assignment,
        lesson_step=step,
        student=user
    )

    # O'quvchining ushbu loyihaga aloqador saqlangan laboratoriya natijalari
    user_labs = LabExperimentSubmission.objects.filter(student=user).order_by('-created_at')[:5]

    # Guruh tekshiruvi (agar guruhli loyiha bo'lsa)
    user_group = assignment.groups.filter(members=user).first()
    if user_group:
        submission.group = user_group
        submission.save()

    if request.method == 'POST':
        title = request.POST.get('title', f"{step.lesson_number}-dars mahsuloti").strip()
        content_text = request.POST.get('content_text', '').strip()
        student_notes = request.POST.get('student_notes', '').strip()
        individual_contribution = request.POST.get('individual_contribution', '').strip()
        linked_lab_id = request.POST.get('linked_lab_id')
        attached_file = request.FILES.get('attached_file')
        is_draft = request.POST.get('is_draft') == 'true'

        if not content_text and not attached_file and not linked_lab_id:
            messages.error(request, "Iltimos, mahsulot matnini, faylni yoki laboratoriya natijasini taqdim eting!")
            return redirect('projects:submit_step', assignment_id=assignment.id, step_id=step.id)

        # Takroriy (double-submit) yuborishdan himoya
        latest_ver = submission.versions.order_by('-version_number').first()
        if latest_ver and not is_draft:
            time_diff = (timezone.now() - latest_ver.submitted_at).total_seconds()
            if time_diff < 5 and latest_ver.content_text == content_text:
                messages.warning(request, "Topshiriq allaqachon qabul qilindi. Qayta yuborish shart emas.")
                return redirect('portfolio:submission_detail', submission_id=submission.id)

        # Fayl turi va hajmi tekshiruvi (Xavfsizlik)
        if attached_file:
            allowed_extensions = ['.pdf', '.txt', '.png', '.jpg', '.jpeg', '.zip', '.docx', '.xlsx']
            ext = os.path.splitext(attached_file.name)[1].lower()
            if ext not in allowed_extensions:
                messages.error(request, f"Noto‘g‘ri fayl formati ({ext}). Faqat PDF, TXT, DOCX, PNG, JPG, ZIP ruxsat etiladi.")
                return redirect('projects:submit_step', assignment_id=assignment.id, step_id=step.id)
            if attached_file.size > 15 * 1024 * 1024:  # 15 MB
                messages.error(request, "Fayl hajmi 15 MB dan oshmasligi kerak!")
                return redirect('projects:submit_step', assignment_id=assignment.id, step_id=step.id)

        # Yangi versiya raqami
        next_version_num = (latest_ver.version_number + 1) if latest_ver else 1

        linked_lab = LabExperimentSubmission.objects.filter(id=linked_lab_id, student=user).first() if linked_lab_id else None

        # Versiyani yaratish
        version = SubmissionVersion.objects.create(
            submission=submission,
            version_number=next_version_num,
            title=title,
            content_text=content_text,
            student_notes=student_notes,
            individual_contribution=individual_contribution,
            linked_lab_submission=linked_lab,
            lab_summary_data=linked_lab.additional_data if linked_lab else {},
            attached_file=attached_file,
            is_draft=is_draft
        )

        if is_draft:
            submission.status = 'draft'
            messages.success(request, f"Topshiriq qoralama (v{next_version_num}) sifatida saqlandi.")
        else:
            submission.status = 'submitted' if next_version_num == 1 else 'resubmitted'
            messages.success(request, f"Topshiriq muvaffaqiyatli topshirildi (v{next_version_num})! O‘qituvchi ko‘rib chiqadi.")

        submission.save()
        return redirect('portfolio:submission_detail', submission_id=submission.id)

    return render(request, 'projects/submit_step.html', {
        'assignment': assignment,
        'step': step,
        'submission': submission,
        'user_labs': user_labs,
        'user_group': user_group
    })
