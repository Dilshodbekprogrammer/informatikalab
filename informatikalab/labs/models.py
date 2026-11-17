from django.db import models
from django.conf import settings


class LabExperimentSubmission(models.Model):
    LAB_TYPE_CHOICES = (
        ('algorithm', 'Algoritmlar laboratoriyasi'),
        ('data', 'Ma’lumotlar laboratoriyasi'),
        ('scratch', 'Scratch vizual dasturlash laboratoriyasi'),
        ('crypto', 'Kriptografiya va axborot xavfsizligi laboratoriyasi'),
        ('network', 'Kompyuter tarmoqlari va marshrutlash simulyatori'),
        ('sorting', 'Saralash va qidiruv algoritmlari vizualizatori'),
        ('logic', 'Mantiqiy elementlar va sxemotexnika laboratoriyasi'),
        ('python', 'Python dasturlash va algoritmlar terminali'),
    )

    ALGORITHM_CHOICES = (
        ('max_two', 'Ikki sonning kattasini topish'),
        ('even_odd', 'Sonning juft yoki toqligini aniqlash'),
        ('sum_n', '1 dan N gacha sonlar yig‘indisini hisoblash'),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lab_experiments',
        verbose_name="O‘quvchi"
    )
    lab_type = models.CharField(max_length=20, choices=LAB_TYPE_CHOICES, verbose_name="Laboratoriya turi")
    algorithm_type = models.CharField(
        max_length=30,
        choices=ALGORITHM_CHOICES,
        blank=True,
        null=True,
        verbose_name="Algoritm turi"
    )
    title = models.CharField(max_length=200, verbose_name="Tajriba sarlavhasi")
    input_data = models.JSONField(default=dict, verbose_name="Kiritilgan boshlang‘ich parametrlar")
    prediction = models.TextField(blank=True, verbose_name="O‘quvchining oldindan taxmini")
    calculated_result = models.TextField(verbose_name="Haqiqiy olingan natija")
    student_explanation = models.TextField(
        verbose_name="O‘quvchi xulosasi: 'Nima o‘zgardi va nima sababdan?'"
    )
    additional_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Qo‘shimcha ko‘rsatkichlar (masalan tejash hisobi, qatorlar)"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Bajarilgan vaqt")

    class Meta:
        verbose_name = "Laboratoriya tajribasi natijasi"
        verbose_name_plural = "Laboratoriya tajribalari natijalari"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.username} - {self.get_lab_type_display()} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
