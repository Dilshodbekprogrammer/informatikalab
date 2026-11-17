from django.db import models
from django.conf import settings
from projects.models import ClassProjectAssignment, ProjectLessonStep, ProjectGroup
from labs.models import LabExperimentSubmission


def submission_file_path(instance, filename):
    return f"submissions/user_{instance.submission.student.id}/step_{instance.submission.lesson_step.id}/{filename}"


class ProjectSubmission(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Qoralama'),
        ('submitted', 'Topshirilgan'),
        ('needs_revision', 'Qayta ishlash tavsiya etildi'),
        ('resubmitted', 'Qayta topshirilgan (yangi versiya)'),
        ('approved', 'Qabul qilindi'),
    )

    assignment = models.ForeignKey(
        ClassProjectAssignment,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name="Loyiha"
    )
    lesson_step = models.ForeignKey(
        ProjectLessonStep,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name="Dars bosqichi"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name="O‘quvchi"
    )
    group = models.ForeignKey(
        ProjectGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='submissions',
        verbose_name="Guruh (agar guruhli bo‘lsa)"
    )
    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Holati"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Loyiha topshirig‘i"
        verbose_name_plural = "Loyiha topshiriqlari"
        unique_together = ('assignment', 'lesson_step', 'student')
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.student.username} - {self.lesson_step.title} ({self.get_status_display()})"

    @property
    def latest_version(self):
        return self.versions.order_by('-version_number').first()

    @property
    def initial_version(self):
        return self.versions.order_by('version_number').first()


class SubmissionVersion(models.Model):
    submission = models.ForeignKey(
        ProjectSubmission,
        on_delete=models.CASCADE,
        related_name='versions',
        verbose_name="Topshiriq"
    )
    version_number = models.PositiveSmallIntegerField(default=1, verbose_name="Versiya raqami")
    title = models.CharField(max_length=200, default="Yaratilgan mahsulot", verbose_name="Mahsulot nomi")
    content_text = models.TextField(verbose_name="Mahsulot / Yechim mazmuni")
    student_notes = models.TextField(blank=True, verbose_name="O‘quvchining izohi")
    individual_contribution = models.TextField(
        blank=True,
        verbose_name="Guruhdagi shaxsiy hissasi (individual hissa)"
    )
    linked_lab_submission = models.ForeignKey(
        LabExperimentSubmission,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='linked_submissions',
        verbose_name="Biriktirilgan laboratoriya tajribasi"
    )
    lab_summary_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Laboratoriya hisob-kitob natijalari nusxasi"
    )
    attached_file = models.FileField(
        upload_to=submission_file_path,
        blank=True,
        null=True,
        verbose_name="Biriktirilgan fayl (PDF, TXT, PNG va b.)"
    )
    is_draft = models.BooleanField(default=False, verbose_name="Qoralama holatdami")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Topshirilgan vaqt")

    class Meta:
        verbose_name = "Topshiriq versiyasi"
        verbose_name_plural = "Topshiriq versiyalari"
        ordering = ['version_number']
        unique_together = ('submission', 'version_number')

    def __str__(self):
        return f"{self.submission.student.username} - {self.submission.lesson_step.title} (v{self.version_number})"


class TeacherFeedback(models.Model):
    version = models.ForeignKey(
        SubmissionVersion,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name="Tegishli versiya"
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name="O‘qituvchi"
    )
    feedback_text = models.TextField(verbose_name="O‘qituvchi izohi va tavsiyasi")
    requires_revision = models.BooleanField(
        default=True,
        verbose_name="Takomillashtirish vazifasi berildimi (qayta ishlash kerakmi)"
    )
    criteria_clarity = models.CharField(max_length=50, blank=True, verbose_name="Mezon: Tushunarlilik")
    criteria_technical = models.CharField(max_length=50, blank=True, verbose_name="Mezon: Texnik to‘g‘rilik")
    criteria_creativity = models.CharField(max_length=50, blank=True, verbose_name="Mezon: Ijodiy yondashuv")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Izoh berilgan vaqt")

    class Meta:
        verbose_name = "O‘qituvchi izohi"
        verbose_name_plural = "O‘qituvchi izohlari"
        ordering = ['-created_at']

    def __str__(self):
        return f"Izoh: v{self.version.version_number} - {self.teacher.username}"


class StudentReflection(models.Model):
    submission = models.OneToOneField(
        ProjectSubmission,
        on_delete=models.CASCADE,
        related_name='reflection',
        verbose_name="Topshiriq"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reflections',
        verbose_name="O‘quvchi"
    )
    what_created = models.TextField(verbose_name="Nima yaratdim?")
    what_error_found = models.TextField(verbose_name="Qaysi xatoni aniqladim?")
    how_improved = models.TextField(verbose_name="Yechimimni qanday yaxshiladim?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yozilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "O‘quvchi refleksiyasi"
        verbose_name_plural = "O‘quvchi refleksiyalari"

    def __str__(self):
        return f"Refleksiya: {self.student.username} - {self.submission.lesson_step.title}"
