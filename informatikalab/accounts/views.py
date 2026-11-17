from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import User, ClassRoom


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.get_full_name() or user.username}!")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('core:home')
        else:
            messages.error(request, "Foydalanuvchi nomi yoki parol noto‘g‘ri!")

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "Tizimdan muvaffaqiyatli chiqdingiz.")
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """O'qituvchi va foydalanuvchilar o'z ma'lumotlari, logini va parolini tahrirlash sahifasi"""
    user = request.user

    if request.method == 'POST':
        action = request.POST.get('action', 'update_profile')

        if action == 'update_profile':
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            new_username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            bio = request.POST.get('bio', '').strip()
            subject = request.POST.get('subject', '').strip()

            if not new_username:
                messages.error(request, "Foydalanuvchi nomi (login) bo‘sh bo‘lishi mumkin emas!")
                return redirect('accounts:profile')

            if new_username != user.username and User.objects.exclude(id=user.id).filter(username=new_username).exists():
                messages.error(request, f"'{new_username}' logini allaqachon mavjud! Iltimos, boshqa login tanlang.")
                return redirect('accounts:profile')

            user.first_name = first_name
            user.last_name = last_name
            user.username = new_username
            user.email = email
            user.phone = phone
            user.bio = bio
            if user.is_teacher and subject:
                user.subject = subject
            user.save()
            messages.success(request, "Profil ma’lumotlaringiz va loginingiz muvaffaqiyatli saqlandi!")
            return redirect('accounts:profile')

        elif action == 'change_password':
            old_password = request.POST.get('old_password', '')
            new_password = request.POST.get('new_password', '')
            confirm_password = request.POST.get('confirm_password', '')

            if not user.check_password(old_password):
                messages.error(request, "Joriy parolingiz noto‘g‘ri kiritildi!")
            elif len(new_password) < 6:
                messages.error(request, "Yangi parol kamida 6 ta belgidan iborat bo‘lishi lozim!")
            elif new_password != confirm_password:
                messages.error(request, "Yangi parol va uning tasdig‘i bir-biriga mos kelmadi!")
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Parolingiz muvaffaqiyatli o‘zgartirildi!")
            return redirect('accounts:profile')

    return render(request, 'accounts/profile.html', {'user': user})


@login_required
def classrooms_list_view(request):
    user = request.user
    if not (user.is_teacher or user.is_admin_role):
        return HttpResponseForbidden("Sizda sinflarni ko‘rish huquqi yo‘q.")

    if user.is_admin_role:
        classrooms = ClassRoom.objects.all().prefetch_related('students', 'teacher')
    else:
        classrooms = ClassRoom.objects.filter(teacher=user).prefetch_related('students')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        grade = request.POST.get('grade', 9)
        academic_year = request.POST.get('academic_year', '2024-2025').strip()
        if name:
            ClassRoom.objects.create(
                name=name,
                grade=int(grade),
                academic_year=academic_year,
                teacher=user
            )
            messages.success(request, f"{name} sinfi muvaffaqiyatli yaratildi.")
            return redirect('accounts:classrooms')

    return render(request, 'accounts/classrooms.html', {'classrooms': classrooms})


@login_required
def classroom_detail_view(request, class_id):
    user = request.user
    classroom = get_object_or_404(ClassRoom, id=class_id)
    if not user.is_admin_role and classroom.teacher != user:
        return HttpResponseForbidden("Siz faqat o‘zingizga biriktirilgan sinflarni ko‘rishingiz mumkin.")

    all_students = User.objects.filter(role='student')

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        action = request.POST.get('action')
        if student_id:
            student = get_object_or_404(User, id=student_id, role='student')
            if action == 'add':
                classroom.students.add(student)
                messages.success(request, f"{student.get_full_name() or student.username} sinfga qo‘shildi.")
            elif action == 'remove':
                classroom.students.remove(student)
                messages.warning(request, f"{student.get_full_name() or student.username} sinfdan chiqarildi.")
            return redirect('accounts:classroom_detail', class_id=class_id)

    return render(request, 'accounts/classroom_detail.html', {
        'classroom': classroom,
        'all_students': all_students,
    })


@login_required
def classroom_add_student_view(request, class_id):
    """O'qituvchi o'z sinfiga yangi o'quvchi hisobi yaratib biriktirishi"""
    user = request.user
    classroom = get_object_or_404(ClassRoom, id=class_id)
    if not user.is_admin_role and classroom.teacher != user:
        return HttpResponseForbidden("Siz faqat o‘zingizning sinfingizga o‘quvchi qo‘sha olasiz.")

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()

        if not username or not password:
            messages.error(request, "O‘quvchi logini va paroli to‘ldirilishi shart!")
            return redirect('accounts:classroom_detail', class_id=class_id)

        if User.objects.filter(username=username).exists():
            messages.error(request, f"'{username}' logini allaqachon band! Boshqa login tanlang.")
            return redirect('accounts:classroom_detail', class_id=class_id)

        if len(password) < 6:
            messages.error(request, "Parol kamida 6 ta belgidan iborat bo‘lishi kerak!")
            return redirect('accounts:classroom_detail', class_id=class_id)

        student = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone=phone,
            role='student'
        )
        student.set_password(password)
        student.save()
        classroom.students.add(student)
        messages.success(request, f"Yangi o‘quvchi {student.get_full_name() or student.username} yaratildi va {classroom.name} sinfiga qo‘shildi!")
        return redirect('accounts:classroom_detail', class_id=class_id)

    return redirect('accounts:classroom_detail', class_id=class_id)


# =========================================================================
# ADMINISTRATOR: FOYDALANUVCHILARNI BOSHQARISH (O'QITUVCHI VA O'QUVCHI QO'SHISH)
# =========================================================================

@login_required
def users_list_view(request):
    """Administrator uchun barcha o'qituvchilar va o'quvchilarni boshqarish sahifasi"""
    if not request.user.is_admin_role:
        return HttpResponseForbidden("Sizda administrator huquqi yo‘q.")

    teachers = User.objects.filter(role='teacher').order_by('first_name', 'last_name')
    students = User.objects.filter(role='student').order_by('first_name', 'last_name')
    classrooms = ClassRoom.objects.all().prefetch_related('students')

    return render(request, 'accounts/users_list.html', {
        'teachers': teachers,
        'students': students,
        'classrooms': classrooms,
        'teachers_count': teachers.count(),
        'students_count': students.count(),
    })


@login_required
def add_teacher_view(request):
    """Administrator tomonidan yangi o'qituvchi qo'shish"""
    if not request.user.is_admin_role:
        return HttpResponseForbidden("Sizda administrator huquqi yo‘q.")

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', 'Informatika').strip()
        bio = request.POST.get('bio', '').strip()

        if not username or not password:
            messages.error(request, "Foydalanuvchi nomi (login) va parol to‘ldirilishi shart!")
            return render(request, 'accounts/add_teacher.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, f"'{username}' logini allaqachon band! Boshqa login tanlang.")
            return render(request, 'accounts/add_teacher.html')

        if len(password) < 6:
            messages.error(request, "Parol kamida 6 ta belgidan iborat bo‘lishi kerak!")
            return render(request, 'accounts/add_teacher.html')

        teacher = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone=phone,
            subject=subject or 'Informatika',
            bio=bio,
            role='teacher',
            is_staff=True
        )
        teacher.set_password(password)
        teacher.save()
        messages.success(request, f"Yangi o‘qituvchi {teacher.get_full_name() or teacher.username} muvaffaqiyatli yaratildi!")
        return redirect('accounts:users_list')

    return render(request, 'accounts/add_teacher.html')


@login_required
def add_student_view(request):
    """Administrator tomonidan yangi o'quvchi qo'shish"""
    if not request.user.is_admin_role:
        return HttpResponseForbidden("Sizda administrator huquqi yo‘q.")

    classrooms = ClassRoom.objects.all()

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        classroom_id = request.POST.get('classroom_id', '')
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()

        if not username or not password:
            messages.error(request, "Foydalanuvchi nomi (login) va parol to‘ldirilishi shart!")
            return render(request, 'accounts/add_student.html', {'classrooms': classrooms})

        if User.objects.filter(username=username).exists():
            messages.error(request, f"'{username}' logini allaqachon band! Boshqa login tanlang.")
            return render(request, 'accounts/add_student.html', {'classrooms': classrooms})

        if len(password) < 6:
            messages.error(request, "Parol kamida 6 ta belgidan iborat bo‘lishi kerak!")
            return render(request, 'accounts/add_student.html', {'classrooms': classrooms})

        student = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone=phone,
            role='student'
        )
        student.set_password(password)
        student.save()

        if classroom_id:
            try:
                classroom = ClassRoom.objects.get(id=classroom_id)
                classroom.students.add(student)
            except ClassRoom.DoesNotExist:
                pass

        messages.success(request, f"Yangi o‘quvchi {student.get_full_name() or student.username} muvaffaqiyatli yaratildi!")
        return redirect('accounts:users_list')

    return render(request, 'accounts/add_student.html', {'classrooms': classrooms})


@login_required
def edit_user_view(request, user_id):
    """Administrator tomonidan foydalanuvchi ma'lumotlarini tahrirlash"""
    if not request.user.is_admin_role:
        return HttpResponseForbidden("Sizda administrator huquqi yo‘q.")

    target_user = get_object_or_404(User, id=user_id)
    classrooms = ClassRoom.objects.all()
    user_classroom = target_user.enrolled_classes.first() if target_user.is_student else None

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        new_username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        bio = request.POST.get('bio', '').strip()
        subject = request.POST.get('subject', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        classroom_id = request.POST.get('classroom_id', '')

        if not new_username:
            messages.error(request, "Foydalanuvchi nomi bo‘sh bo‘lishi mumkin emas!")
            return redirect('accounts:edit_user', user_id=target_user.id)

        if new_username != target_user.username and User.objects.exclude(id=target_user.id).filter(username=new_username).exists():
            messages.error(request, f"'{new_username}' logini allaqachon band!")
            return redirect('accounts:edit_user', user_id=target_user.id)

        target_user.first_name = first_name
        target_user.last_name = last_name
        target_user.username = new_username
        target_user.email = email
        target_user.phone = phone
        target_user.bio = bio
        if target_user.is_teacher and subject:
            target_user.subject = subject

        if new_password:
            if len(new_password) < 6:
                messages.error(request, "Parol kamida 6 ta belgidan iborat bo‘lishi kerak!")
                return redirect('accounts:edit_user', user_id=target_user.id)
            target_user.set_password(new_password)
            messages.info(request, f"{target_user.username} paroli yangilandi.")

        target_user.save()

        if target_user.is_student:
            target_user.enrolled_classes.clear()
            if classroom_id:
                try:
                    c = ClassRoom.objects.get(id=classroom_id)
                    c.students.add(target_user)
                except ClassRoom.DoesNotExist:
                    pass

        messages.success(request, f"{target_user.get_full_name() or target_user.username} ma’lumotlari muvaffaqiyatli yangilandi!")
        return redirect('accounts:users_list')

    return render(request, 'accounts/edit_user.html', {
        'target_user': target_user,
        'classrooms': classrooms,
        'user_classroom': user_classroom,
    })


@login_required
def delete_user_view(request, user_id):
    """Administrator tomonidan foydalanuvchini o'chirish"""
    if not request.user.is_admin_role:
        return HttpResponseForbidden("Sizda administrator huquqi yo‘q.")

    target_user = get_object_or_404(User, id=user_id)
    if target_user.id == request.user.id:
        messages.error(request, "O‘z hisobingizni o‘chira olmaysiz!")
        return redirect('accounts:users_list')

    if request.method == 'POST':
        name = target_user.get_full_name() or target_user.username
        target_user.delete()
        messages.success(request, f"{name} tizimdan muvaffaqiyatli o‘chirildi.")
        return redirect('accounts:users_list')

    return render(request, 'accounts/delete_user_confirm.html', {'target_user': target_user})
