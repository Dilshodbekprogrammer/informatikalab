from django.db import models
from django.conf import settings
from accounts.models import ClassRoom


class ProjectTemplate(models.Model):
    title = models.CharField(max_length=255, verbose_name="Loyiha nomi")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")
    topic = models.CharField(max_length=255, verbose_name="Mavzu")
    description = models.TextField(verbose_name="Loyiha tavsifi")
    grade = models.PositiveSmallIntegerField(default=9, verbose_name="Sinf")
    total_lessons = models.PositiveSmallIntegerField(default=4, verbose_name="Darslar soni")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Namunaviy loyiha shabloni"
        verbose_name_plural = "Namunaviy loyiha shablonlari"

    def __str__(self):
        return self.title


class ProjectLessonStep(models.Model):
    project_template = models.ForeignKey(
        ProjectTemplate,
        on_delete=models.CASCADE,
        related_name='steps',
        verbose_name="Loyiha"
    )
    lesson_number = models.PositiveSmallIntegerField(verbose_name="Dars raqami (1..4)")
    title = models.CharField(max_length=255, verbose_name="Dars mavzusi")
    instructions = models.TextField(verbose_name="Tayyor ko‘rsatma")
    task_details = models.TextField(verbose_name="Topshiriq mazmuni")
    expected_artifact = models.TextField(verbose_name="Topshiriladigan mahsulot tavsifi")
    RECOMMENDED_LAB_CHOICES = (
        ('algorithm', 'Algoritmlar laboratoriyasi'),
        ('data', 'Ma’lumotlar laboratoriyasi'),
        ('scratch', 'Scratch vizual dasturlash laboratoriyasi'),
        ('crypto', 'Kriptografiya va axborot xavfsizligi laboratoriyasi'),
        ('network', 'Kompyuter tarmoqlari va marshrutlash simulyatori'),
        ('sorting', 'Saralash va qidiruv algoritmlari vizualizatori'),
        ('logic', 'Mantiqiy elementlar va sxemotexnika laboratoriyasi'),
        ('python', 'Python dasturlash va algoritmlar terminali'),
    )

    recommended_lab = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=RECOMMENDED_LAB_CHOICES,
        verbose_name="Bog‘liq interaktiv laboratoriya"
    )

    class Meta:
        verbose_name = "Loyiha dars bosqichi"
        verbose_name_plural = "Loyiha dars bosqichlari"
        ordering = ['project_template', 'lesson_number']
        unique_together = ('project_template', 'lesson_number')

    def __str__(self):
        return f"{self.project_template.title} - {self.lesson_number}-dars: {self.title}"


class ClassProjectAssignment(models.Model):
    project_template = models.ForeignKey(
        ProjectTemplate,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name="Loyiha shabloni"
    )
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE,
        related_name='project_assignments',
        verbose_name="Biriktirilgan sinf"
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned_projects',
        verbose_name="Mas'ul o‘qituvchi"
    )
    is_group_project = models.BooleanField(
        default=False,
        verbose_name="Guruhli loyiha formati"
    )
    deadline = models.DateField(
        null=True,
        blank=True,
        verbose_name="Topshirish muddati (deadline)"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Biriktirilgan vaqt")

    class Meta:
        verbose_name = "Sinf loyihasi biriktirmasi"
        verbose_name_plural = "Sinf loyihalari biriktirmalari"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.project_template.title} -> {self.classroom.name}"


class ProjectGroup(models.Model):
    assignment = models.ForeignKey(
        ClassProjectAssignment,
        on_delete=models.CASCADE,
        related_name='groups',
        verbose_name="Sinf loyihasi"
    )
    name = models.CharField(max_length=150, verbose_name="Guruh nomi")
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='led_project_groups',
        verbose_name="Guruh yetakchisi"
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='student_project_groups',
        verbose_name="Guruh a'zolari"
    )
    role_distribution = models.TextField(
        verbose_name="Vazifalar taqsimoti (har bir o‘quvchining roli)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Loyiha guruhi"
        verbose_name_plural = "Loyiha guruhlari"

    def __str__(self):
        return f"{self.name} ({self.assignment.classroom.name})"
