from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'O‘qituvchi'),
        ('student', 'O‘quvchi'),
        ('admin', 'Administrator'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
        verbose_name="Foydalanuvchi roli"
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon raqami")
    bio = models.TextField(blank=True, verbose_name="Qisqa ma'lumot")
    subject = models.CharField(max_length=100, default="Informatika", verbose_name="Fan")

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    @property
    def is_teacher(self):
        return self.role == 'teacher'

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_admin_role(self):
        return self.role == 'admin' or self.is_superuser

    def __str__(self):
        full = self.get_full_name()
        return f"{full} ({self.get_role_display()})" if full else f"{self.username} ({self.get_role_display()})"


class ClassRoom(models.Model):
    name = models.CharField(max_length=50, verbose_name="Sinf nomi (masalan: 9-A)")
    grade = models.PositiveSmallIntegerField(default=9, verbose_name="Sinf bosqichi")
    academic_year = models.CharField(max_length=20, default="2024-2025", verbose_name="O‘quv yili")
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='teaching_classes',
        limit_choices_to={'role': 'teacher'},
        verbose_name="Mas'ul o‘qituvchi"
    )
    students = models.ManyToManyField(
        User,
        related_name='enrolled_classes',
        limit_choices_to={'role': 'student'},
        blank=True,
        verbose_name="Sinf o‘quvchilari"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Sinf"
        verbose_name_plural = "Sinflar"
        ordering = ['grade', 'name']

    def __str__(self):
        return f"{self.name} ({self.teacher.get_full_name() or self.teacher.username})"
