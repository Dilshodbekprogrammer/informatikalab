import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from accounts.models import ClassRoom
from methods.models import TeachingMethod
from projects.models import ClassProjectAssignment, ProjectLessonStep
from portfolio.models import ProjectSubmission
from .models import LessonPlan, LessonStage


@login_required
def lessons_list_view(request):
    user = request.user
    if user.is_student:
        return redirect('lessons:student_lessons')

    if user.is_admin_role:
        lessons = LessonPlan.objects.all().select_related('teacher', 'classroom', 'method')
    else:
        lessons = LessonPlan.objects.filter(teacher=user).select_related('classroom', 'method')

    return render(request, 'lessons/list.html', {'lessons': lessons})


@login_required
def student_lessons_view(request):
    user = request.user
    # O'quvchi o'ziga biriktirilgan sinf darslarini ko'radi
    enrolled_classes = user.enrolled_classes.all()
    assigned_lessons = LessonPlan.objects.filter(
        classroom__in=enrolled_classes,
        status='assigned'
    ).select_related('teacher', 'classroom', 'method').order_by('-updated_at')

    return render(request, 'lessons/student_lessons.html', {
        'lessons': assigned_lessons,
        'enrolled_classes': enrolled_classes
    })


@login_required
def lesson_create_view(request):
    user = request.user
    if not (user.is_teacher or user.is_admin_role):
        return HttpResponseForbidden("Faqat o‘qituvchilar dars konstruktoridan foydalanishi mumkin.")

    classrooms = ClassRoom.objects.filter(teacher=user) if not user.is_admin_role else ClassRoom.objects.all()
    methods = TeachingMethod.objects.filter(is_active=True).order_by('order')

    selected_method_id = request.GET.get('method')
    selected_method = None
    if selected_method_id:
        selected_method = TeachingMethod.objects.filter(id=selected_method_id).first()

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        classroom_id = request.POST.get('classroom_id')
        method_id = request.POST.get('method_id')
        learning_objective = request.POST.get('learning_objective', '').strip()
        duration_minutes = int(request.POST.get('duration_minutes', 45))
        available_equipment = request.POST.get('available_equipment', '').strip()
        activity_type = request.POST.get('activity_type', 'individual')
        status = request.POST.get('status', 'draft')

        classroom = None
        if classroom_id:
            classroom = get_object_or_404(ClassRoom, id=classroom_id)
            if not user.is_admin_role and classroom.teacher != user:
                return HttpResponseForbidden("Siz faqat o‘zingizga biriktirilgan sinfga dars biriktira olasiz.")

        method = TeachingMethod.objects.filter(id=method_id).first() if method_id else None

        stage_names = request.POST.getlist('stage_name[]')
        stage_durations = request.POST.getlist('stage_duration[]')
        stage_teacher_actions = request.POST.getlist('stage_teacher_action[]')
        stage_student_actions = request.POST.getlist('stage_student_action[]')
        stage_tasks = request.POST.getlist('stage_task[]')
        stage_resources = request.POST.getlist('stage_resource[]')
        stage_products = request.POST.getlist('stage_product[]')

        valid_stages = [n.strip() for n in stage_names if n.strip()]
        total_stage_time = 0
        for i in range(len(stage_names)):
            if stage_names[i].strip():
                try:
                    total_stage_time += int(stage_durations[i])
                except (IndexError, ValueError):
                    total_stage_time += 5

        # Bug 6: Sinfga biriktirish (assigned) holatida majburiy tekshiruvlar
        if status == 'assigned':
            errors = []
            if not classroom:
                errors.append("Darsni sinfga biriktirish uchun sinf tanlanishi shart!")
            if not learning_objective:
                errors.append("Kuzatiladigan o‘quv maqsadi bo‘sh bo‘lmasligi kerak!")
            if len(valid_stages) == 0:
                errors.append("Kamida bitta dars bosqichi kiritilishi shart!")

            if errors:
                for err in errors:
                    messages.error(request, err)
                status = 'draft'
            elif total_stage_time != duration_minutes:
                messages.warning(
                    request,
                    f"Diqqat: Bosqichlar vaqti yig‘indisi ({total_stage_time} daqiqa) rejalashtirilgan dars davomiyligi ({duration_minutes} daqiqa) bilan teng emas."
                )

        lesson = LessonPlan.objects.create(
            teacher=user,
            classroom=classroom,
            method=method,
            title=title,
            learning_objective=learning_objective,
            duration_minutes=duration_minutes,
            available_equipment=available_equipment,
            activity_type=activity_type,
            status=status
        )

        for i in range(len(stage_names)):
            name = stage_names[i].strip()
            if name:
                try:
                    dur = int(stage_durations[i])
                except (IndexError, ValueError):
                    dur = 5
                LessonStage.objects.create(
                    lesson=lesson,
                    order=i + 1,
                    name=name,
                    duration_minutes=dur,
                    teacher_action=stage_teacher_actions[i] if i < len(stage_teacher_actions) else '',
                    student_action=stage_student_actions[i] if i < len(stage_student_actions) else '',
                    task_description=stage_tasks[i] if i < len(stage_tasks) else '',
                    resources=stage_resources[i] if i < len(stage_resources) else '',
                    expected_product=stage_products[i] if i < len(stage_products) else '',
                )

        if status == 'draft':
            messages.success(request, f"Dars rejasi qoralama sifatida saqlandi: {lesson.title}")
        else:
            messages.success(request, f"Dars muvaffaqiyatli sinfga biriktirildi: {lesson.title}")

        return redirect('lessons:detail', lesson_id=lesson.id)

    # Shablon bosqichlarini JSON formatida uzatish
    methods_json = {}
    for m in methods:
        methods_json[str(m.id)] = {
            'title': m.title,
            'stages': m.default_stages_template
        }

    return render(request, 'lessons/create.html', {
        'classrooms': classrooms,
        'methods': methods,
        'selected_method': selected_method,
        'methods_json': json.dumps(methods_json)
    })


@login_required
def lesson_edit_view(request, lesson_id):
    user = request.user
    lesson = get_object_or_404(LessonPlan, id=lesson_id)
    if not user.is_admin_role and lesson.teacher != user:
        return HttpResponseForbidden("Siz faqat o‘zingiz yaratgan darslarni tahrirlashingiz mumkin.")

    classrooms = ClassRoom.objects.filter(teacher=user) if not user.is_admin_role else ClassRoom.objects.all()
    methods = TeachingMethod.objects.filter(is_active=True).order_by('order')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        classroom_id = request.POST.get('classroom_id')
        method_id = request.POST.get('method_id')
        learning_objective = request.POST.get('learning_objective', '').strip()
        duration_minutes = int(request.POST.get('duration_minutes', 45))
        available_equipment = request.POST.get('available_equipment', '').strip()
        activity_type = request.POST.get('activity_type', 'individual')
        status = request.POST.get('status', 'draft')

        classroom = None
        if classroom_id:
            classroom = get_object_or_404(ClassRoom, id=classroom_id)
            if not user.is_admin_role and classroom.teacher != user:
                return HttpResponseForbidden("Siz faqat o‘zingizga biriktirilgan sinfga dars biriktira olasiz.")

        stage_names = request.POST.getlist('stage_name[]')
        stage_durations = request.POST.getlist('stage_duration[]')
        stage_teacher_actions = request.POST.getlist('stage_teacher_action[]')
        stage_student_actions = request.POST.getlist('stage_student_action[]')
        stage_tasks = request.POST.getlist('stage_task[]')
        stage_resources = request.POST.getlist('stage_resource[]')
        stage_products = request.POST.getlist('stage_product[]')

        valid_stages = [n.strip() for n in stage_names if n.strip()]
        total_stage_time = 0
        for i in range(len(stage_names)):
            if stage_names[i].strip():
                try:
                    total_stage_time += int(stage_durations[i])
                except (IndexError, ValueError):
                    total_stage_time += 5

        # Bug 6: Sinfga biriktirish holatida tekshiruvlar
        if status == 'assigned':
            errors = []
            if not classroom:
                errors.append("Darsni sinfga biriktirish uchun sinf tanlanishi shart!")
            if not learning_objective:
                errors.append("Kuzatiladigan o‘quv maqsadi bo‘sh bo‘lmasligi kerak!")
            if len(valid_stages) == 0:
                errors.append("Kamida bitta dars bosqichi kiritilishi shart!")

            if errors:
                for err in errors:
                    messages.error(request, err)
                status = 'draft'
            elif total_stage_time != duration_minutes:
                messages.warning(
                    request,
                    f"Diqqat: Bosqichlar vaqti yig‘indisi ({total_stage_time} daqiqa) rejalashtirilgan dars davomiyligi ({duration_minutes} daqiqa) bilan teng emas."
                )

        lesson.title = title
        lesson.classroom = classroom
        lesson.method = TeachingMethod.objects.filter(id=method_id).first() if method_id else None
        lesson.learning_objective = learning_objective
        lesson.duration_minutes = duration_minutes
        lesson.available_equipment = available_equipment
        lesson.activity_type = activity_type
        lesson.status = status
        lesson.save()

        # Eski bosqichlarni yangilash
        lesson.stages.all().delete()

        for i in range(len(stage_names)):
            name = stage_names[i].strip()
            if name:
                try:
                    dur = int(stage_durations[i])
                except (IndexError, ValueError):
                    dur = 5
                LessonStage.objects.create(
                    lesson=lesson,
                    order=i + 1,
                    name=name,
                    duration_minutes=dur,
                    teacher_action=stage_teacher_actions[i] if i < len(stage_teacher_actions) else '',
                    student_action=stage_student_actions[i] if i < len(stage_student_actions) else '',
                    task_description=stage_tasks[i] if i < len(stage_tasks) else '',
                    resources=stage_resources[i] if i < len(stage_resources) else '',
                    expected_product=stage_products[i] if i < len(stage_products) else '',
                )

        messages.success(request, f"Dars o‘zgarishlari saqlandi: {lesson.title}")
        return redirect('lessons:detail', lesson_id=lesson.id)

    return render(request, 'lessons/edit.html', {
        'lesson': lesson,
        'classrooms': classrooms,
        'methods': methods,
    })


@login_required
def lesson_duplicate_view(request, lesson_id):
    user = request.user
    lesson = get_object_or_404(LessonPlan, id=lesson_id)
    if not user.is_admin_role and lesson.teacher != user:
        return HttpResponseForbidden("Siz faqat o‘z darsingizdan nusxa olishingiz mumkin.")

    new_lesson = LessonPlan.objects.create(
        teacher=user,
        classroom=lesson.classroom,
        method=lesson.method,
        title=f"{lesson.title} (Nusxa)",
        target_grade=lesson.target_grade,
        learning_objective=lesson.learning_objective,
        duration_minutes=lesson.duration_minutes,
        available_equipment=lesson.available_equipment,
        activity_type=lesson.activity_type,
        status='draft'
    )

    for st in lesson.stages.all():
        LessonStage.objects.create(
            lesson=new_lesson,
            order=st.order,
            name=st.name,
            duration_minutes=st.duration_minutes,
            teacher_action=st.teacher_action,
            student_action=st.student_action,
            task_description=st.task_description,
            resources=st.resources,
            expected_product=st.expected_product,
        )

    messages.success(request, f"Darsdan yangi nusxa (qoralama) yaratildi: {new_lesson.title}")
    return redirect('lessons:edit', lesson_id=new_lesson.id)


@login_required
def lesson_detail_view(request, lesson_id):
    user = request.user
    lesson = get_object_or_404(LessonPlan, id=lesson_id)

    # Kirish huquqi tekshiruvi: O'qituvchi o'z darsini yoki admin barcha darsni; o'quvchi faqat o'z sinfiga biriktirilgan darsni
    if user.is_student:
        if not lesson.classroom or not lesson.classroom.students.filter(id=user.id).exists():
            return HttpResponseForbidden("Sizda bu darsni ko‘rish huquqi yo‘q (faqat o‘z sinfingiz darslariga kira olasiz).")
        if lesson.status == 'draft':
            return HttpResponseForbidden("Ushbu dars hozircha qoralama holatida va o‘quvchilarga taqdim etilmagan.")
    elif not user.is_admin_role and lesson.teacher != user:
        return HttpResponseForbidden("Siz faqat o‘zingizga tegishli darslarni ko‘rishingiz mumkin.")

    # Bug 5: Darsdan loyiha va topshiriqlargacha bo'lgan bog'lanish
    related_assignments = []
    student_submissions_map = {}
    if lesson.classroom:
        related_assignments = ClassProjectAssignment.objects.filter(
            classroom=lesson.classroom
        ).select_related('project_template', 'teacher').prefetch_related('project_template__steps')

        if user.is_student:
            subs = ProjectSubmission.objects.filter(
                assignment__in=related_assignments,
                student=user
            ).select_related('lesson_step')
            for sub in subs:
                student_submissions_map[sub.lesson_step.id] = sub

    return render(request, 'lessons/detail.html', {
        'lesson': lesson,
        'related_assignments': related_assignments,
        'student_submissions_map': student_submissions_map,
    })


@login_required
def lesson_print_view(request, lesson_id):
    user = request.user
    lesson = get_object_or_404(LessonPlan, id=lesson_id)

    # Bug 1b: Chop etish sahifasida to'liq huquq tekshiruvi
    if user.is_admin_role:
        pass
    elif user.is_teacher:
        if lesson.teacher != user:
            return HttpResponseForbidden("Siz faqat o‘z darsingizni chop etishingiz mumkin.")
    elif user.is_student:
        if not lesson.classroom or not lesson.classroom.students.filter(id=user.id).exists():
            return HttpResponseForbidden("Siz faqat o‘z sinfingiz darslarini chop etishingiz mumkin.")
        if lesson.status == 'draft':
            return HttpResponseForbidden("Ushbu dars hozircha qoralama holatida va o‘quvchilarga taqdim etilmagan.")
    else:
        return HttpResponseForbidden("Ruxsat berilmagan.")

    return render(request, 'lessons/print_view.html', {'lesson': lesson})
