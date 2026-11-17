from django.db import models


class TeachingMethod(models.Model):
    title = models.CharField(max_length=200, verbose_name="Metod nomi")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    short_description = models.TextField(verbose_name="Sodda tushuntirish")
    applicable_when = models.TextField(verbose_name="Qaysi vaziyatda qo‘llanishi")
    teacher_role = models.TextField(verbose_name="O‘qituvchining vazifalari")
    student_role = models.TextField(verbose_name="O‘quvchining vazifalari")
    lesson_stages_overview = models.TextField(verbose_name="Dars bosqichlari umumiy tavsifi")
    sample_cs_case = models.TextField(verbose_name="Informatika fanidan amaliy misol (9-sinf)")
    required_equipment = models.TextField(verbose_name="Kerakli qurilmalar va materiallar")
    
    # Xorijiy tajriba
    foreign_country = models.CharField(max_length=100, verbose_name="Xorijiy davlat (Finlandiya, Estoniya, Angliya)")
    foreign_practice_case = models.TextField(verbose_name="Xorijiy amaliyotdan tekshirilgan faktik misol")
    source_citation = models.TextField(verbose_name="Rasmiy manba va havola")
    source_url = models.URLField(max_length=500, blank=True, verbose_name="Manba URL manzili")
    adaptation_recommendation = models.TextField(
        verbose_name="O‘zbekiston maktab sharoitiga moslashtirish tavsiyasi (fakt bilan ajratilgan)"
    )

    # Shablon bosqichlari (JSON: [{'order': 1, 'name': '...', 'duration': 10, 'teacher_action': '...', 'student_action': '...', 'task': '...', 'product': '...'}])
    default_stages_template = models.JSONField(
        default=list,
        verbose_name="Dars konstruktori uchun standart bosqichlar shabloni"
    )

    badge_color = models.CharField(max_length=30, default="blue", verbose_name="Belgi rangi (UI)")
    order = models.PositiveSmallIntegerField(default=1, verbose_name="Tartib raqami")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi")

    class Meta:
        verbose_name = "O‘qitish metodi"
        verbose_name_plural = "Metodlar kutubxonasi"
        ordering = ['order', 'title']

    def __str__(self):
        return self.title
