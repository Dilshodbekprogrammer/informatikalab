from django.db import models
from django.conf import settings
from accounts.models import ClassRoom
from methods.models import TeachingMethod


class LessonPlan(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Qoralama'),
        ('assigned', 'Sinfga biriktirilgan'),
        ('completed', 'Yakunlangan'),
    )

    ACTIVITY_CHOICES = (
        ('individual', 'Individual faoliyat'),
        ('group', 'Guruhli faoliyat'),
        ('mixed', 'Aralash (individual va guruhli)'),
    )

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lesson_plans',
        verbose_name="O‘qituvchi"
    )
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lessons',
        verbose_name="Biriktirilgan sinf"
    )
    method = models.ForeignKey(
        TeachingMethod,
        on_delete=models.SET_NULL,
        null=True,
        related_name='lessons',
        verbose_name="Tanlangan metod"
    )
    title = models.CharField(max_length=250, verbose_name="Dars mavzusi")
    target_grade = models.PositiveSmallIntegerField(default=9, verbose_name="Sinf")
    learning_objective = models.TextField(
        verbose_name="Kuzatiladigan o‘quv maqsadi (SMART shaklida)"
    )
    duration_minutes = models.PositiveSmallIntegerField(
        default=45,
        verbose_name="Dars davomiyligi (daqiqa)"
    )
    available_equipment = models.CharField(
        max_length=255,
        default="Kompyuter xonasi, proyektor, lokal tarmoq",
        verbose_name="Mavjud qurilmalar va sharoit"
    )
    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_CHOICES,
        default='individual',
        verbose_name="Faoliyat turi"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Holati"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Oxirgi tahrir")

    class Meta:
        verbose_name = "Dars loyihasi"
        verbose_name_plural = "Dars loyihalari"
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    @property
    def total_stages_duration(self):
        return sum(stage.duration_minutes for stage in self.stages.all())

    @property
    def is_time_balanced(self):
        return self.total_stages_duration == self.duration_minutes

    @property
    def time_diff(self):
        return self.duration_minutes - self.total_stages_duration


class LessonStage(models.Model):
    lesson = models.ForeignKey(
        LessonPlan,
        on_delete=models.CASCADE,
        related_name='stages',
        verbose_name="Dars rejasi"
    )
    order = models.PositiveSmallIntegerField(default=1, verbose_name="Bosqich tartibi")
    name = models.CharField(max_length=150, verbose_name="Bosqich nomi")
    duration_minutes = models.PositiveSmallIntegerField(default=5, verbose_name="Vaqt (daqiqa)")
    teacher_action = models.TextField(verbose_name="O‘qituvchi harakati")
    student_action = models.TextField(verbose_name="O‘quvchi harakati")
    task_description = models.TextField(verbose_name="Topshiriq tavsifi")
    resources = models.CharField(max_length=255, blank=True, verbose_name="Resurslar va vositalar")
    expected_product = models.TextField(verbose_name="Kutiladigan mahsulot")

    class Meta:
        verbose_name = "Dars bosqichi"
        verbose_name_plural = "Dars bosqichlari"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.order}. {self.name} ({self.duration_minutes} daqiqa)"
