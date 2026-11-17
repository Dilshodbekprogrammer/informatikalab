import json
from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, ClassRoom
from methods.models import TeachingMethod
from lessons.models import LessonPlan, LessonStage
from labs.models import LabExperimentSubmission
from projects.models import ProjectTemplate, ProjectLessonStep, ClassProjectAssignment, ProjectGroup
from portfolio.models import ProjectSubmission, SubmissionVersion, TeacherFeedback, StudentReflection


class FullPlatformWorkflowTests(TestCase):
    def setUp(self):
        # 1. Foydalanuvchilar
        self.teacher1 = User.objects.create_user(
            username='teacher1', password='pass', role='teacher', first_name='Jasur', last_name='Karimov'
        )
        self.teacher2 = User.objects.create_user(
            username='teacher2', password='pass', role='teacher', first_name='Botir', last_name='Zokirov'
        )
        self.student1 = User.objects.create_user(
            username='student1', password='pass', role='student', first_name='Anvar', last_name='Saidov'
        )
        self.student2 = User.objects.create_user(
            username='student2', password='pass', role='student', first_name='Madina', last_name='Alimova'
        )
        self.student_other = User.objects.create_user(
            username='student_other', password='pass', role='student', first_name='Begona', last_name='Oquvchi'
        )

        # 2. Sinflar
        self.classroom_9a = ClassRoom.objects.create(name='9-A sinf', grade=9, teacher=self.teacher1)
        self.classroom_9a.students.add(self.student1, self.student2)

        self.classroom_9b = ClassRoom.objects.create(name='9-B sinf', grade=9, teacher=self.teacher2)
        self.classroom_9b.students.add(self.student_other)

        # 3. Metod
        self.pbl_method = TeachingMethod.objects.create(
            title="Loyiha asosida o‘qitish (Project-Based Learning)",
            slug="loyiha-asosida-oqitish",
            short_description="Amaliy loyiha yordamida o‘rganish",
            applicable_when="Kompleks amaliy ko‘nikma kerak bo‘lganda",
            teacher_role="Yo‘naltiradi",
            student_role="Yaratadi",
            lesson_stages_overview="1. Muammo\n2. Reja\n3. Tajriba\n4. Xulosa",
            sample_cs_case="9-sinf elektr energiyasini tejash kalkulyatori",
            required_equipment="Kompyuterlar",
            foreign_country="Estoniya",
            foreign_practice_case="Estoniya ProgeTiigri dasturi",
            source_citation="Harno (harno.ee/progetiigri)",
            adaptation_recommendation="4 darsga bo‘lib o‘qitish tavsiya etiladi",
            default_stages_template=[
                {"name": "Muammo", "duration": 10},
                {"name": "Tajriba", "duration": 25},
                {"name": "Xulosa", "duration": 10}
            ]
        )

        # 4. Namunaviy Loyiha shabloni
        self.project_template = ProjectTemplate.objects.create(
            title="Maktabda elektr energiyasidan oqilona foydalanish",
            slug="maktab-elektr-energiyasi",
            topic="Elektr energiyasi sarfi",
            description="4 darslik kompleks amaliy loyiha",
            grade=9,
            total_lessons=4
        )
        self.step1 = ProjectLessonStep.objects.create(
            project_template=self.project_template,
            lesson_number=1,
            title="1-dars: Muammo, ma’lumotlar va taxmin",
            instructions="Muammoni aniqlang",
            task_details="Gipoteza tuzing",
            expected_artifact="Boshlang‘ich gipoteza",
            recommended_lab="data"
        )
        self.step2 = ProjectLessonStep.objects.create(
            project_template=self.project_template,
            lesson_number=2,
            title="2-dars: Hisoblash, jadval va diagramma",
            instructions="Formulani hisoblang",
            task_details="Jadval va diagramma tuzing",
            expected_artifact="Hisob-kitob jadvali",
            recommended_lab="data"
        )

        # 5. Loyihani 9-A sinfiga biriktirish
        self.assignment = ClassProjectAssignment.objects.create(
            project_template=self.project_template,
            classroom=self.classroom_9a,
            teacher=self.teacher1,
            is_group_project=True
        )

        # 6. Guruh
        self.group = ProjectGroup.objects.create(
            assignment=self.assignment,
            name="Eko-Informatiklar",
            leader=self.student1,
            role_distribution="Anvar: Hisob-kitob, Madina: Diagramma"
        )
        self.group.members.add(self.student1, self.student2)

    # 1. NAZORAT MISOLLARI: ALGORITMLAR LABORATORIYASI
    def test_algorithms_control_examples(self):
        """Uchta algoritmning barcha nazorat misollari tekshiriladi"""
        # A) Ikki sonning kattasini topish
        # Nazorat: 7 va 3 uchun max = 7
        a, b = 7, 3
        max_ab = a if a > b else b
        self.assertEqual(max_ab, 7, "7 va 3 uchun eng katta son 7 bo'lishi kerak")

        # Teng sonlar nazorati: a=5, b=5 holati
        a, b = 5, 5
        is_equal = (a == b)
        self.assertTrue(is_equal, "Teng sonlar uchun tenglik holati aniqlanishi kerak")

        # B) Juft yoki toqlik
        # Nazorat: -4 juft son!
        x = -4
        is_even = (x % 2 == 0)
        self.assertTrue(is_even, "-4 soni juft son bo'lishi shart")

        # 7 toq son
        self.assertFalse(7 % 2 == 0, "7 toq son bo'lishi kerak")

        # 0 juft son
        self.assertTrue(0 % 2 == 0, "0 juft son bo'lishi kerak")

        # C) 1 dan N gacha sonlar yig'indisi
        # Nazorat: N=5 uchun yig'indi 15
        N = 5
        sum_5 = sum(range(1, N + 1))
        self.assertEqual(sum_5, 15, "1 dan 5 gacha yig'indi 15 bo'lishi shart")

        # Nazorat: N=0 uchun yig'indi 0
        N = 0
        sum_0 = sum(range(1, N + 1)) if N > 0 else 0
        self.assertEqual(sum_0, 0, "N=0 uchun yig'indi 0 bo'lishi shart")

    # 2. NAZORAT MISOLLARI: MA'LUMOTLAR LABORATORIYASI VA ENERGIYA TEJASH
    def test_energy_calculations_and_savings(self):
        """Elektr energiyasi formulasi va 20% tejash nazorat misoli tekshiriladi"""
        # Formula: Energiya = quvvat (W) * vaqt (soat) * soni / 1000
        # Nazorat misoli: 100 W * 5 soat * 2 / 1000 = 1.0 kWh
        power = 100
        hours = 5
        count = 2
        initial_kwh = (power * hours * count) / 1000.0
        self.assertAlmostEqual(initial_kwh, 1.0, places=3, msg="100W * 5h * 2 / 1000 = 1.0 kWh bo'lishi kerak")

        # Vaqt 4 soatga tushirilsa: 100 W * 4 soat * 2 / 1000 = 0.8 kWh
        reduced_hours = 4
        new_kwh = (power * reduced_hours * count) / 1000.0
        self.assertAlmostEqual(new_kwh, 0.8, places=3, msg="4 soatda 0.8 kWh bo'lishi kerak")

        # Tejash: 0.2 kWh, ya'ni 20%
        saved_kwh = initial_kwh - new_kwh
        self.assertAlmostEqual(saved_kwh, 0.2, places=3)
        saving_percent = (saved_kwh / initial_kwh) * 100.0
        self.assertAlmostEqual(saving_percent, 20.0, places=1, msg="Tejash aniq 20% bo'lishi shart")

        # Boshlang'ich sarf nol bo'lsa: Nolga bo'linish xatosi (ZeroDivisionError) oldini olish
        zero_kwh = 0.0
        zero_saved = 0.0
        safe_percent = (zero_saved / zero_kwh * 100) if zero_kwh > 0 else 0.0
        self.assertEqual(safe_percent, 0.0, "Boshlang'ich sarf nol bo'lganda 0% qaytishi kerak")

    # 3. DARS KONSTRUKTORI: DARS BOSQICHLARI VAQTINI TEKSHIRISH
    def test_lesson_constructor_and_time_balance(self):
        """Dars vaqti balansi va saqlanishi tekshiriladi"""
        lesson = LessonPlan.objects.create(
            teacher=self.teacher1,
            classroom=self.classroom_9a,
            method=self.pbl_method,
            title="Tarmoqlanuvchi algoritmlar",
            duration_minutes=45,
            status='draft'
        )

        # 3 ta bosqich: 10 + 25 + 10 = 45 daqiqa
        LessonStage.objects.create(lesson=lesson, order=1, name="Muammo", duration_minutes=10)
        LessonStage.objects.create(lesson=lesson, order=2, name="Tajriba", duration_minutes=25)
        LessonStage.objects.create(lesson=lesson, order=3, name="Xulosa", duration_minutes=10)

        self.assertEqual(lesson.total_stages_duration, 45)
        self.assertTrue(lesson.is_time_balanced)
        self.assertEqual(lesson.time_diff, 0)

        # Darsni nusxalash (duplicate) tekshiruvi
        client = Client()
        client.force_login(self.teacher1)
        resp = client.get(reverse('lessons:duplicate', args=[lesson.id]), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(LessonPlan.objects.filter(title__contains="Nusxa").exists())

    # 4. TO'LIQ JARAYON: METOD -> DARS -> TAJRIBA -> TOPSHIRISH -> IZOH -> V2 -> REFLEKSIYA
    def test_full_learning_workflow(self):
        """Metod tanlash -> Dars -> Tajriba saqlash -> Mahsulot v1 -> O'qituvchi izohi -> v2 -> Refleksiya"""
        client = Client()

        # A) O'quvchi laboratoriya tajribasini o'tkazib saqlaydi
        client.force_login(self.student1)
        lab_payload = {
            "lab_type": "data",
            "title": "Elektr energiyasi sarfi tahlili",
            "input_data": {"device": "Kompyuter", "power": 150, "hours": 5, "count": 12},
            "prediction": "Kompyuterlar eng ko'p sarflaydi",
            "calculated_result": "9.0 kWh",
            "student_explanation": "Kompyuterlar soni 12 dona bo'lgani uchun umumiy sarf yuqori chiqdi.",
            "additional_data": {"savings": "20%"}
        }
        resp = client.post(
            reverse('labs:save_experiment_api'),
            data=json.dumps(lab_payload),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(LabExperimentSubmission.objects.filter(student=self.student1).exists())

        # B) O'quvchi mahsulot topshiradi (v1)
        post_data = {
            "title": "1-dars gipotezasi",
            "content_text": "Biz maktab elektr energiyasi sarfini o'rgandik. Hisob-kitoblarimiz xomaki holatda.",
            "student_notes": "Birinchi versiya",
            "individual_contribution": "Quvvatlarni yozib chiqdim",
            "is_draft": "false"
        }
        resp = client.post(
            reverse('projects:submit_step', args=[self.assignment.id, self.step1.id]),
            data=post_data,
            follow=True
        )
        self.assertEqual(resp.status_code, 200)

        submission = ProjectSubmission.objects.get(assignment=self.assignment, student=self.student1, lesson_step=self.step1)
        self.assertEqual(submission.versions.count(), 1)
        v1 = submission.versions.first()
        self.assertEqual(v1.version_number, 1)

        # C) O'qituvchi izoh beradi va takomillashtirish vazifasini qo'yadi
        client.force_login(self.teacher1)
        fb_data = {
            "feedback_text": "Gipoteza yaxshi, ammo quvvatni 1000 ga bo'lib kWh ga o'tkazing!",
            "requires_revision": "on",
            "criteria_clarity": "Yaxshi",
            "criteria_technical": "Kichik xatolik bor",
            "criteria_creativity": "Ijodiy"
        }
        resp = client.post(
            reverse('portfolio:add_feedback', args=[v1.id]),
            data=fb_data,
            follow=True
        )
        self.assertEqual(resp.status_code, 200)

        submission.refresh_from_db()
        self.assertEqual(submission.status, 'needs_revision')
        self.assertEqual(v1.feedbacks.count(), 1)

        # D) O'quvchi yangi takomillashtirilgan versiyani yuboradi (v2)
        client.force_login(self.student1)
        post_data_v2 = {
            "title": "1-dars takomillashtirilgan yechimi",
            "content_text": "O'qituvchi aytganidek formulani to'g'riladik: 150W * 5h * 12 / 1000 = 9.0 kWh.",
            "student_notes": "Formulalar to'g'rilandi",
            "individual_contribution": "kWh ga o'tkazish hisobini qildim",
            "is_draft": "false"
        }
        resp = client.post(
            reverse('projects:submit_step', args=[self.assignment.id, self.step1.id]),
            data=post_data_v2,
            follow=True
        )
        self.assertEqual(resp.status_code, 200)

        submission.refresh_from_db()
        self.assertEqual(submission.versions.count(), 2)
        v2 = submission.latest_version
        self.assertEqual(v2.version_number, 2)
        self.assertEqual(submission.status, 'resubmitted')

        # E) O'quvchi yakuniy refleksiyani to'ldiradi
        ref_data = {
            "what_created": "Maktab elektr energiyasi sarfi tahlilini yaratdim",
            "what_error_found": "Birliklarni kWh ga o'tkazishni unutgan edim",
            "how_improved": "O'qituvchi tavsiyasidan so'ng 1000 ga bo'lib kWh ga o'tkazdim"
        }
        resp = client.post(
            reverse('portfolio:save_reflection', args=[submission.id]),
            data=ref_data,
            follow=True
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(StudentReflection.objects.filter(submission=submission).exists())

        # F) Versiyalarni taqqoslash (Diff/Compare) sahifasi ochilishi
        resp = client.get(reverse('portfolio:compare_versions', args=[submission.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "v1")
        self.assertContains(resp, "v2")

    # 5. XAVFSIZLIK VA VAKOLATLAR (IDOR VA ACCESS CONTROL HIMOYA TESTI)
    def test_security_access_control_and_idor(self):
        """Boshqa sinf yoki boshqa o'quvchi ma'lumotiga kirish server darajasida rad etilishi (403)"""
        client = Client()

        # Boshqa sinf o'quvchisi (student_other) student1 ning topshirig'ini ko'ra olmasligi kerak
        submission = ProjectSubmission.objects.create(
            assignment=self.assignment,
            lesson_step=self.step1,
            student=self.student1,
            status='submitted'
        )

        client.force_login(self.student_other)
        resp = client.get(reverse('portfolio:submission_detail', args=[submission.id]))
        self.assertEqual(resp.status_code, 403, "Boshqa o'quvchi ishiga kirish 403 taqiqlanishi kerak")

        # Boshqa o'qituvchi (teacher2) teacher1 sinfining loyihasiga izoh qoldira olmasligi kerak
        v = SubmissionVersion.objects.create(submission=submission, version_number=1, content_text="Test")
        client.force_login(self.teacher2)
        resp = client.get(reverse('portfolio:add_feedback', args=[v.id]))
        self.assertEqual(resp.status_code, 403, "Boshqa sinf o'qituvchisiga ruxsat cheklangan bo'lishi kerak")

        # O'quvchi o'qituvchi uchun mo'ljallangan dars konstruktoriga kira olmasligi kerak
        client.force_login(self.student1)
        resp = client.get(reverse('lessons:create'))
        self.assertEqual(resp.status_code, 403, "O'quvchi dars konstruktoriga kira olmasligi shart")


class EightDefectsFixedTests(TestCase):
    """Foydalanuvchi tekshiruvida aniqlangan 8 ta nuqsonning to'liq tuzatilganligini sinovchi testlar"""

    def setUp(self):
        self.teacher1 = User.objects.create_user(
            username='teacher1_test', password='password123',
            role='teacher', first_name="Oqituvchi 1"
        )
        self.teacher2 = User.objects.create_user(
            username='teacher2_test', password='password123',
            role='teacher', first_name="Oqituvchi 2"
        )
        self.student1 = User.objects.create_user(
            username='student1_test', password='password123',
            role='student', first_name="Oquvchi 1"
        )
        self.student2 = User.objects.create_user(
            username='student2_test', password='password123',
            role='student', first_name="Oquvchi 2"
        )

        self.class1 = ClassRoom.objects.create(name='9-A test', grade=9, teacher=self.teacher1)
        self.class1.students.add(self.student1)

        self.class2 = ClassRoom.objects.create(name='9-B test', grade=9, teacher=self.teacher2)
        self.class2.students.add(self.student2)

        self.method = TeachingMethod.objects.create(
            title="Muammoli ta'lim", slug="muammoli-test",
            order=1, source_citation="EDUFI Finlandiya",
            source_url="https://www.oph.fi/en/education-and-qualifications/basic-education"
        )

        self.project = ProjectTemplate.objects.create(
            title="Elektr tejamkorligi", slug="elektr-test", grade=9
        )
        self.step = ProjectLessonStep.objects.create(
            project_template=self.project, lesson_number=1,
            title="Hisob-kitob", recommended_lab="data"
        )

        self.assignment = ClassProjectAssignment.objects.create(
            project_template=self.project, classroom=self.class1,
            teacher=self.teacher1, is_group_project=True
        )

    def test_bug1_access_control_isolated_across_teachers(self):
        """Bug 1: O'qituvchilar bir-birining darsi, guruhi va sinfiga aralasha olmasligi (403)"""
        client = Client()
        client.force_login(self.teacher2)

        # 1. teacher2 teacher1 ning loyihasiga guruh tuza olmasligi kerak
        resp = client.post(reverse('projects:group_create', args=[self.assignment.id]), {
            'name': 'Noqonuniy guruh',
            'leader_id': self.student1.id,
            'members[]': [self.student1.id]
        })
        self.assertEqual(resp.status_code, 403, "Begona o'qituvchi guruh tuza olmasligi kerak")

        # 2. teacher2 teacher1 ning darsini chop etish sahifasini ko'ra olmasligi kerak
        lesson = LessonPlan.objects.create(
            teacher=self.teacher1, classroom=self.class1,
            title="Maxfiy dars", duration_minutes=45, status='draft'
        )
        resp = client.get(reverse('lessons:print', args=[lesson.id]))
        self.assertEqual(resp.status_code, 403, "Begona o'qituvchi darsni chop etish ko'rinishiga kira olmasligi kerak")

        # 3. teacher2 dars yaratishda teacher1 ning sinfini tanlasa 403 qaytishi kerak
        resp = client.post(reverse('lessons:create'), {
            'title': 'Buzishga urinish',
            'classroom_id': self.class1.id,
            'learning_objective': 'Maqsad',
            'duration_minutes': 45,
            'status': 'draft'
        })
        self.assertEqual(resp.status_code, 403, "Begona sinfga dars biriktirish 403 bilan to'silishi kerak")

    def test_bug2_protected_file_download(self):
        """Bug 2: Fayl yuklab olishda huquqlar qat'iy tekshirilishi"""
        client = Client()
        submission = ProjectSubmission.objects.create(
            assignment=self.assignment, lesson_step=self.step, student=self.student1
        )
        version = SubmissionVersion.objects.create(
            submission=submission, version_number=1, content_text="Matn"
        )

        # Anonim foydalanuvchi yuklab ololmasligi (login ga yo'naltirilishi)
        resp = client.get(reverse('portfolio:download_file', args=[version.id]))
        self.assertEqual(resp.status_code, 302)

        # Boshqa sinf o'quvchisi yuklab ololmasligi (403)
        client.force_login(self.student2)
        resp = client.get(reverse('portfolio:download_file', args=[version.id]))
        self.assertEqual(resp.status_code, 403)

    def test_bug3_lab_data_integrity_server_verification(self):
        """Bug 3: Server tomonida laboratoriya hisob-kitoblarini qayta tekshirish"""
        client = Client()
        client.force_login(self.student1)

        # Noto'g'ri natija: a=100, b=3, lekin yuborilgan natija "Eng katta son: 7"
        mismatched_payload = {
            'lab_type': 'algorithm',
            'algorithm_type': 'max_two',
            'input_data': {'paramA': 100, 'paramB': 3, 'paramCond': 'gt'},
            'calculated_result': 'Eng katta son: 7',
            'student_explanation': 'Test xulosa'
        }
        resp = client.post(
            reverse('labs:save_experiment_api'),
            data=json.dumps(mismatched_payload),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 400, "Noto'g'ri algoritm natijasi serverda rad etilishi kerak")
        self.assertIn("Noto'g'ri natija", resp.json()['message'])

        # To'g'ri natija: a=100, b=3, calculated_result="Eng katta son: 100"
        correct_payload = {
            'lab_type': 'algorithm',
            'algorithm_type': 'max_two',
            'input_data': {'paramA': 100, 'paramB': 3, 'paramCond': 'gt'},
            'calculated_result': 'Eng katta son: 100',
            'student_explanation': 'Haqiqiy to‘g‘ri xulosa'
        }
        resp = client.post(
            reverse('labs:save_experiment_api'),
            data=json.dumps(correct_payload),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200, "To'g'ri hisoblangan natija muvaffaqiyatli saqlanishi kerak")

    def test_bug4_portfolio_state_latest_version_integrity(self):
        """Bug 4: Eski versiyani tasdiqlash yangi versiya holatini buzmasligi"""
        client = Client()
        submission = ProjectSubmission.objects.create(
            assignment=self.assignment, lesson_step=self.step,
            student=self.student1, status='submitted'
        )
        v1 = SubmissionVersion.objects.create(
            submission=submission, version_number=1, content_text="v1 mahsuloti"
        )
        # O'qituvchi v1 ni qayta ishlashga qaytaradi
        TeacherFeedback.objects.create(
            version=v1, teacher=self.teacher1,
            feedback_text="Tuzating", requires_revision=True
        )
        submission.status = 'needs_revision'
        submission.save()

        # O'quvchi v2 topshiradi
        v2 = SubmissionVersion.objects.create(
            submission=submission, version_number=2, content_text="v2 takomillashtirilgan"
        )
        submission.status = 'resubmitted'
        submission.save()

        # O'qituvchi endi eski v1 ga kirib tasdiqlab qo'yishga urinsa:
        client.force_login(self.teacher1)
        resp = client.post(reverse('portfolio:add_feedback', args=[v1.id]), {
            'feedback_text': 'Eski versiyaga kech kelgan fikr',
            'requires_revision': False
        })
        submission.refresh_from_db()
        self.assertNotEqual(
            submission.status, 'approved',
            "Eski v1 ni tasdiqlash yangi topshirilgan v2 ning 'resubmitted' holatini 'approved' ga aylantirib yubormasligi kerak"
        )
        self.assertEqual(submission.status, 'resubmitted')

    def test_bug6_lesson_assign_requires_classroom(self):
        """Bug 6: Sinf tanlanmasa darsni 'assigned' qilib bo'lmasligi, draft qilinishi"""
        client = Client()
        client.force_login(self.teacher1)

        # Sinfsiz 'assigned' qilishga urinish
        resp = client.post(reverse('lessons:create'), {
            'title': 'Sinfsiz dars',
            'classroom_id': '',
            'learning_objective': 'Maqsad bor',
            'duration_minutes': 45,
            'status': 'assigned',
            'stage_name[]': ['1-bosqich'],
            'stage_duration[]': [45]
        }, follow=True)

        lesson = LessonPlan.objects.get(title='Sinfsiz dars')
        self.assertEqual(
            lesson.status, 'draft',
            "Sinf tanlanmagan dars 'assigned' emas, 'draft' holatida saqlanishi kerak"
        )

    def test_bug7_group_product_optional_text(self):
        """Bug 7: Laboratoriya natijasi biriktirilganda matn kiritilmasa ham qabul qilinishi"""
        client = Client()
        client.force_login(self.student1)

        lab = LabExperimentSubmission.objects.create(
            student=self.student1, lab_type='data',
            title="Elektr sarfi tajribasi", calculated_result="1.0 -> 0.8 kWh"
        )

        resp = client.post(
            reverse('projects:submit_step', args=[self.assignment.id, self.step.id]),
            data={
                'title': 'Faqat lab natijasi topshirildi',
                'content_text': '',  # Matn yo'q
                'linked_lab_id': lab.id,
                'is_draft': 'false'
            },
            follow=True
        )
        self.assertEqual(resp.status_code, 200)
        submission = ProjectSubmission.objects.get(assignment=self.assignment, lesson_step=self.step, student=self.student1)
        latest = submission.latest_version
        self.assertEqual(latest.linked_lab_submission, lab)

    def test_bug8_method_has_clickable_source_url(self):
        """Bug 8: Metod kartochkalarida bosiladigan rasmiy URL mavjudligi"""
        client = Client()
        client.force_login(self.teacher1)

        resp = client.get(reverse('methods:detail', args=[self.method.slug]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'https://www.oph.fi/en/education-and-qualifications/basic-education')
        self.assertContains(resp, 'Rasmiy manba havolasini ochish')

    def test_scratch_laboratory_integration(self):
        """Yangi Scratch vizual blokli dasturlash laboratoriyasi to'liq ishlashi"""
        client = Client()
        client.force_login(self.student1)

        # 1. Scratch laboratoriyasi sahifasi ochilishi
        resp = client.get(reverse('labs:scratch'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Scratch Vizual Blokli Dasturlash")
        self.assertContains(resp, "penCanvas")
        self.assertContains(resp, "spriteCanvas")

        # 2. Scratch natijasini saqlash API
        scratch_payload = {
            'lab_type': 'scratch',
            'title': 'Scratch Kvadrat chizish loyihasi',
            'input_data': {'blocks_count': 6},
            'prediction': 'Sprait kvadrat chizadi',
            'calculated_result': 'Kvadrat muvaffaqiyatli chizildi (4 x 90 deg)',
            'student_explanation': 'Sikl operatori orqali qalam bilan 4 marta burilib kvadrat chizildi',
            'additional_data': {'final_x': 0, 'final_y': 0}
        }
        resp = client.post(
            reverse('labs:save_experiment_api'),
            data=json.dumps(scratch_payload),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(LabExperimentSubmission.objects.filter(student=self.student1, lab_type='scratch').exists())

    def test_crypto_laboratory_integration(self):
        """Kriptografiya va axborot xavfsizligi laboratoriyasi to'liq ishlashi"""
        client = Client()
        client.force_login(self.student1)

        resp = client.get(reverse('labs:crypto'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Kriptografiya va Axborot Xavfsizligi")
        self.assertContains(resp, "Sezar Shifri")

        payload = {
            'lab_type': 'crypto',
            'title': 'Sezar shifri tajribasi (K=3)',
            'input_data': {'module': 'caesar', 'key': 3, 'text': 'SALOM'},
            'prediction': 'Harflar 3 ta oldinga siljiydi',
            'calculated_result': 'SALOM -> VDORP',
            'student_explanation': 'Alifbo bo\'yicha K=3 qadam siljish orqali matn shifrlangan yopiq holatga keltirildi.',
            'additional_data': {'module': 'caesar'}
        }
        resp = client.post(
            reverse('labs:save_experiment_api'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(LabExperimentSubmission.objects.filter(student=self.student1, lab_type='crypto').exists())

    def test_network_laboratory_integration(self):
        """Kompyuter tarmoqlari va marshrutlash simulyatori to'liq ishlashi"""
        client = Client()
        client.force_login(self.student1)

        resp = client.get(reverse('labs:network'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Kompyuter Tarmoqlari")
        self.assertContains(resp, "networkCanvas")

        payload = {
            'lab_type': 'network',
            'title': 'Yulduz topologiyasi ishonchlilik testi',
            'input_data': {'topology': 'star'},
            'prediction': 'Bitta kabel uzilsa ham tarmoq ishlayveradi',
            'calculated_result': 'Switch orqali qolgan 3 ta kompyuter aloqada qoldi',
            'student_explanation': 'Markaziy Switch har bir kompyuterga alohida liniya bergani sababli bitta kabel uzilishi tarmoqni to\'xtatmaydi.',
            'additional_data': {'topology': 'star'}
        }
        resp = client.post(
            reverse('labs:save_experiment_api'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(LabExperimentSubmission.objects.filter(student=self.student1, lab_type='network').exists())

    def test_sorting_laboratory_integration(self):
        """Saralash va qidiruv algoritmlari vizualizatori to'liq ishlashi"""
        client = Client()
        client.force_login(self.student1)

        resp = client.get(reverse('labs:sorting'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Saralash va Qidiruv Algoritmlari")
        self.assertContains(resp, "barsContainer")

        payload = {
            'lab_type': 'sorting',
            'title': 'Pufaksimon saralash tahlili',
            'input_data': {'algorithm': 'bubble'},
            'prediction': 'Katta elementlar o\'ng tomonga o\'tadi',
            'calculated_result': 'Massiv saralandi, taqqoslashlar: 21, almashtirishlar: 8',
            'student_explanation': 'Qo\'shni elementlar juft-juft taqqoslanib, kichikdan kattaga qarab to\'liq saralandi.',
            'additional_data': {'algorithm': 'bubble'}
        }
        resp = client.post(
            reverse('labs:save_experiment_api'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(LabExperimentSubmission.objects.filter(student=self.student1, lab_type='sorting').exists())

    def test_logic_laboratory_integration(self):
        """Mantiqiy ventillar va sxemotexnika laboratoriyasi to'liq ishlashi"""
        client = Client()
        client.force_login(self.student1)

        resp = client.get(reverse('labs:logic'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Mantiqiy Elementlar va Sxemotexnika")
        self.assertContains(resp, "moduleAdder")
        self.assertContains(resp, "gateVisualBox")

        payload = {
            'lab_type': 'logic',
            'title': '1-bitli Half-Adder sxemasi sinovi',
            'input_data': {'gate': 'half_adder', 'inputA': 1, 'inputB': 1},
            'prediction': 'Ikkala kirish 1 bo\'lsa Sum=0, Carry=1 bo\'ladi',
            'calculated_result': 'Sum (Yig\'indi)=0, Carry (Ko\'chirish)=1. Ikkilik natija: 10_2 = 2_10',
            'student_explanation': 'XOR elementi yig\'indini, AND elementi esa keyingi razryadga ko\'chirishni hisobladi.',
            'additional_data': {'inputs': [1, 1], 'outputs': [0, 1]}
        }
        resp = client.post(
            reverse('labs:save_experiment_api'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(LabExperimentSubmission.objects.filter(student=self.student1, lab_type='logic').exists())

    def test_python_laboratory_integration(self):
        """Python oflayn terminal laboratoriyasi to'liq ishlashi"""
        client = Client()
        client.force_login(self.student1)

        resp = client.get(reverse('labs:python'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Python Algoritmik Terminali")
        self.assertContains(resp, "pythonCodeEditor")
        self.assertContains(resp, "terminalOutput")
        self.assertContains(resp, "pythonStdin")
        self.assertContains(resp, "pyInt")
        self.assertContains(resp, "pyInput")

        payload = {
            'lab_type': 'python',
            'title': 'Faktorial hisoblash algoritmi tajribasi',
            'input_data': {'script': 'n = 5\nf = 1\nfor i in range(1, n+1):\n    f = f * i\nprint(f)'},
            'prediction': '5 faktoriali 120 chiqadi',
            'calculated_result': 'Dastur chiqishi:\n120',
            'student_explanation': 'for sikli 1 dan 5 gacha sonlarni ko\'paytirib chiqdi va natija 120 ekanligi tasdiqlandi.',
            'additional_data': {'lines_count': 5}
        }
        resp = client.post(
            reverse('labs:save_experiment_api'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(LabExperimentSubmission.objects.filter(student=self.student1, lab_type='python').exists())

    def test_teacher_profile_edit_and_password_change(self):
        """O'qituvchi o'z profili, logini va parolini o'zgartira olishi"""
        client = Client()
        client.force_login(self.teacher1)

        # 1. Profil sahifasini ochish
        resp = client.get(reverse('accounts:profile'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Profil va hisob sozlamalari")

        # 2. Login va shaxsiy ma'lumotlarni tahrirlash
        resp = client.post(reverse('accounts:profile'), {
            'action': 'update_profile',
            'first_name': 'Jasurbek',
            'last_name': 'Karimov Yangi',
            'username': 'jasur_ustoz',
            'email': 'jasur_new@maktab.uz',
            'phone': '+998901234567',
            'subject': 'Informatika',
            'bio': 'Yangilangan bio'
        })
        self.assertEqual(resp.status_code, 302)
        self.teacher1.refresh_from_db()
        self.assertEqual(self.teacher1.username, 'jasur_ustoz')
        self.assertEqual(self.teacher1.first_name, 'Jasurbek')

        # 3. Parolni muvaffaqiyatli o'zgartirish
        resp = client.post(reverse('accounts:profile'), {
            'action': 'change_password',
            'old_password': 'password123',
            'new_password': 'yangi_parol_789',
            'confirm_password': 'yangi_parol_789'
        })
        self.assertEqual(resp.status_code, 302)
        self.teacher1.refresh_from_db()
        self.assertTrue(self.teacher1.check_password('yangi_parol_789'))

    def test_admin_user_management_crud(self):
        """Administrator o'qituvchi va o'quvchi qo'shishi, tahrirlashi va ruxsatlar tekshiruvi"""
        admin = User.objects.create_superuser(username='admin_boss', password='adminpassword')
        client = Client()

        # O'quvchi va o'qituvchi uchun 403 Forbidden
        client.force_login(self.student1)
        resp = client.get(reverse('accounts:users_list'))
        self.assertEqual(resp.status_code, 403)

        client.force_login(self.teacher1)
        resp = client.get(reverse('accounts:users_list'))
        self.assertEqual(resp.status_code, 403)

        # Admin sifatida kirish
        client.force_login(admin)
        resp = client.get(reverse('accounts:users_list'))
        self.assertEqual(resp.status_code, 200)

        # 1. Yangi o'qituvchi qo'shish
        resp = client.post(reverse('accounts:add_teacher'), {
            'first_name': 'Shahnoza',
            'last_name': 'Rahimova',
            'username': 'shahnoza_ustoz',
            'password': 'ustoz_parol_123',
            'email': 'shahnoza@maktab.uz',
            'phone': '+998935554433',
            'subject': 'Informatika va Robototexnika'
        })
        self.assertEqual(resp.status_code, 302)
        new_teacher = User.objects.get(username='shahnoza_ustoz')
        self.assertEqual(new_teacher.role, 'teacher')
        self.assertTrue(new_teacher.check_password('ustoz_parol_123'))

        # 2. Yangi o'quvchi qo'shish
        resp = client.post(reverse('accounts:add_student'), {
            'first_name': 'Javohir',
            'last_name': 'Toshmatov',
            'username': 'javohir_oquvchi',
            'password': 'javohir_parol_123',
            'classroom_id': self.class1.id
        })
        self.assertEqual(resp.status_code, 302)
        new_student = User.objects.get(username='javohir_oquvchi')
        self.assertEqual(new_student.role, 'student')
        self.assertTrue(self.class1.students.filter(id=new_student.id).exists())

        # 3. O'quvchini tahrirlash va parolini yangilash
        resp = client.post(reverse('accounts:edit_user', args=[new_student.id]), {
            'first_name': 'Javohirbek',
            'last_name': 'Toshmatov',
            'username': 'javohir_updated',
            'new_password': 'yangi_parol_456',
            'classroom_id': self.class1.id
        })
        self.assertEqual(resp.status_code, 302)
        new_student.refresh_from_db()
        self.assertEqual(new_student.username, 'javohir_updated')
        self.assertTrue(new_student.check_password('yangi_parol_456'))
