import json
from django.core.management.base import BaseCommand
from accounts.models import User, ClassRoom
from methods.models import TeachingMethod
from lessons.models import LessonPlan, LessonStage
from projects.models import ProjectTemplate, ProjectLessonStep, ClassProjectAssignment, ProjectGroup
from portfolio.models import ProjectSubmission, SubmissionVersion, TeacherFeedback, StudentReflection


class Command(BaseCommand):
    help = "InformatikaLab platformasi uchun namunaviy ma'lumotlarni yuklaydi."

    def handle(self, *args, **options):
        self.stdout.write("Boshlang‘ich ma'lumotlarni yuklash boshlandi...")

        # 1. Foydalanuvchilar yaratish
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Administrator',
                'last_name': 'Tizim',
                'email': 'admin@informatikalab.uz',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()

        teacher_user, _ = User.objects.get_or_create(
            username='oqituvchi',
            defaults={
                'first_name': 'Jasur',
                'last_name': 'Karimov',
                'email': 'jasur@maktab.uz',
                'role': 'teacher',
                'subject': 'Informatika va axborot texnologiyalari',
                'bio': '9-sinf informatika fani o‘qituvchisi. Zamonaviy pedagogik metodlar targ‘ibotchisi.',
            }
        )
        teacher_user.set_password('oqituvchi123')
        teacher_user.save()

        teacher2, _ = User.objects.get_or_create(
            username='malika_oqituvchi',
            defaults={
                'first_name': 'Malika',
                'last_name': 'Akbarova',
                'email': 'malika@maktab.uz',
                'role': 'teacher',
                'subject': 'Informatika va robototexnika',
                'bio': 'Informatika fani o‘qituvchisi. STEAM va algoritmik loyihalar bo‘yicha ekspert.',
            }
        )
        teacher2.set_password('oqituvchi123')
        teacher2.save()

        student1, _ = User.objects.get_or_create(
            username='oquvchi1',
            defaults={
                'first_name': 'Anvar',
                'last_name': 'Saidov',
                'email': 'anvar@maktab.uz',
                'role': 'student',
            }
        )
        student1.set_password('oquvchi123')
        student1.save()

        student2, _ = User.objects.get_or_create(
            username='oquvchi2',
            defaults={
                'first_name': 'Madina',
                'last_name': 'Alimova',
                'email': 'madina@maktab.uz',
                'role': 'student',
            }
        )
        student2.set_password('oquvchi123')
        student2.save()

        student3, _ = User.objects.get_or_create(
            username='nodir',
            defaults={
                'first_name': 'Nodirbek',
                'last_name': 'Zokirov',
                'email': 'nodir@maktab.uz',
                'role': 'student',
            }
        )
        student3.set_password('oquvchi123')
        student3.save()

        student4, _ = User.objects.get_or_create(
            username='dilnoza',
            defaults={
                'first_name': 'Dilnoza',
                'last_name': 'Rahimova',
                'email': 'dilnoza@maktab.uz',
                'role': 'student',
            }
        )
        student4.set_password('oquvchi123')
        student4.save()

        # 2. Sinflar yaratish
        class_9a, _ = ClassRoom.objects.get_or_create(
            name='9-A sinf',
            defaults={
                'grade': 9,
                'academic_year': '2024-2025',
                'teacher': teacher_user,
            }
        )
        class_9a.students.set([student1, student2, student3])
        class_9a.save()

        class_9b, _ = ClassRoom.objects.get_or_create(
            name='9-B sinf',
            defaults={
                'grade': 9,
                'academic_year': '2024-2025',
                'teacher': teacher2,
            }
        )
        class_9b.students.set([student4])
        class_9b.save()

        # 3. Beshta Metod kartochkasi (Xorijiy tajribalar va tekshirilgan manbalar bilan)
        methods_data = [
            {
                "title": "Loyiha asosida o‘qitish (Project-Based Learning - PBL)",
                "slug": "loyiha-asosida-oqitish",
                "order": 1,
                "badge_color": "blue",
                "short_description": "O‘quvchilar real hayotiy muammoni hal qilish maqsadida mustaqil ravishda bir necha dars davomida amaliy dasturiy yoki intellektual mahsulot yaratadilar.",
                "applicable_when": "Mavzu bo‘yicha nazariy bilimlar o‘zlashtirilib, ularni amaliyotda birlashtirish, jamoaviy ishlash va dasturlash orqali to‘liq ishlaydigan mahsulot yaratish kerak bo‘lganda.",
                "teacher_role": "• Loyiha mavzusi va mezonlarini belgilaydi;\n• O‘quvchilarni guruhlarga taqsimlaydi va yo‘naltiradi;\n• Har bir oraliq bosqichda metodik maslahat beradi va oraliq izoh qoldiradi.",
                "student_role": "• Muammoni tahlil qiladi va talablarni shakllantiradi;\n• Vazifalarni guruh ichida taqsimlab dasturiy yechim yaratadi;\n• O‘qituvchi fikridan so‘ng mahsulotni takomillashtiradi.",
                "lesson_stages_overview": "1. Muammo va g‘oya tanlash (10 daqiqa)\n2. Tahlil va arxitektura rejalashtirish (10 daqiqa)\n3. Amaliy ishlab chiqish (15 daqiqa)\n4. Taqdimot va refleksiya (10 daqiqa)",
                "sample_cs_case": "9-sinfda 'Maktabda elektr energiyasidan oqilona foydalanish' mavzusida ma'lumotlar tahlili va tejash kalkulyatorini yaratish.",
                "required_equipment": "Kompyuter xonasi, lokal tarmoq, brauzer, matn muharriri yoki Python muhiti.",
                "foreign_country": "Estoniya",
                "foreign_practice_case": "Estoniyaning Ta'lim va Yoshlar Departamenti (Harno) tomonidan boshqariladigan 'ProgeTiigri' (Dasturlash yo‘lbarsi) milliy dasturida informatika fani sinf bosqichlarida aynan real amaliy loyihalar (web, sensorlar, ma'lumotlar tahlili) orqali o‘qitiladi.",
                "source_citation": "Harno (Hariduse ja Noorteamet) - ProgeTiigri programm (rasmiy manba: harno.ee/progetiigri)",
                "source_url": "https://harno.ee/progetiigri",
                "adaptation_recommendation": "O‘zbekiston maktablaridagi 45 daqiqalik dars tartibiga moslashtirish uchun yirik loyiha 4 ta alohida darsga bo‘linadi (1-dars: gipoteza, 2-dars: hisob-kitob, 3-dars: algoritm, 4-dars: takomillashtirish).",
                "default_stages_template": [
                    {"name": "Loyiha muammosi va g‘oya bilan tanishish", "duration": 5, "teacher_action": "Muammoni taqdim etadi va maqsadni belgilaydi", "student_action": "Guruhda muammoni muhokama qiladi", "task": "Gipoteza tuzish", "resource": "InformatikaLab", "product": "Loyiha rejasi"},
                    {"name": "Rejalashtirish va rollar taqsimoti", "duration": 10, "teacher_action": "Guruhlar faoliyatini muvofiqlashtiradi", "student_action": "Vazifalarni taqsimlaydi va algoritmni chizadi", "task": "Rollar jadvali", "resource": "Loyiha ustaxonasi", "product": "Vazifalar xaritasi"},
                    {"name": "Laboratoriyada amaliy ishlab chiqish", "duration": 20, "teacher_action": "Texnik maslahatlar beradi", "student_action": "Simulyator va jadvalda amaliy yechimni yaratadi", "task": "Dasturiy yechim", "resource": "Interaktiv laboratoriya", "product": "Dastlabki mahsulot (v1)"},
                    {"name": "Taqdimot va oraliq baholash", "duration": 10, "teacher_action": "Oraliq izoh va tavsiyalar beradi", "student_action": "Natijani namoyish qiladi va izohni qayd etadi", "task": "Himoya", "resource": "Portfolio", "product": "Taqriz va tavsiya"}
                ]
            },
            {
                "title": "Muammoli ta’lim (Problem-Based Learning)",
                "slug": "muammoli-talim",
                "order": 2,
                "badge_color": "green",
                "short_description": "O‘quvchiga tayyor qoida berilmaydi, balki kutilmagan ziddiyatli muammo qo‘yiladi. O‘quvchi mustaqil izlanish orqali qonuniyatni kashf etadi.",
                "applicable_when": "Yangi algoritmik tushunchalarni (masalan tarmoqlanish, sikllar yoki shartli operatorlar) chuqur anglash va mantiqiy tafakkurni charxlash zarur bo‘lganda.",
                "teacher_role": "• Ziddiyatli muammoli vaziyatni yaratadi;\n• O‘quvchilar gipotezalarini yo‘naltiradi;\n• Natijalarni umumlashtirishga ko‘maklashadi.",
                "student_role": "• Muammoni tahlil qiladi va taxmin (gipoteza) ilgari suradi;\n• Tajriba orqali o‘z taxminini tekshiradi;\n• Xulosa chiqaradi.",
                "lesson_stages_overview": "1. Muammoli savol qo‘yish (5 daqiqa)\n2. Gipoteza ishlab chiqish (10 daqiqa)\n3. Tajribaviy tekshirish (15 daqiqa)\n4. Yechim va xulosa (15 daqiqa)",
                "sample_cs_case": "9-sinfda: 'Nega manfiy son (-4) ikkiga bo‘linganda dastur xato bermaydi va u qanday toifa son hisoblanadi?' ziddiyati orqali butun sonlar arifmetikasi va qoldiq operatorini o‘rganish.",
                "required_equipment": "Proyektor, doska, interaktiv laboratoriya kompyuterlari.",
                "foreign_country": "Finlandiya",
                "foreign_practice_case": "Finlandiya Milliy Ta'lim Agentligi (EDUFI - Opetushallitus) asosiy o‘quv dasturida (OPS 2016) 'Ilmiöpohjainen oppiminen' (Phenomenon-based learning) tamoyili asosida o‘quvchilar real hayotiy hodisalarni muammo qilib tadqiq etadilar.",
                "source_citation": "Finnish National Agency for Education (EDUFI) - National Core Curriculum for Basic Education (rasmiy manba: oph.fi)",
                "source_url": "https://www.oph.fi/en/curriculum-basics-and-local-curricula",
                "adaptation_recommendation": "Muammoli savol informatika xonasining kundalik sarfi yoki maktab serverining yuklamasi kabi lokal misollar asosida beriladi, shunda o‘quvchilar nazariyani kundalik hayot bilan bog‘laydilar.",
                "default_stages_template": [
                    {"name": "Muammoli savol qo‘yish", "duration": 5, "teacher_action": "Ziddiyatli misolni namoyish etadi", "student_action": "Ziddiyatni anglaydi va savollar beradi", "task": "Savolni shakllantirish", "resource": "Doska/Proyektor", "product": "Muammo ta'rifi"},
                    {"name": "Gipoteza va taxmin", "duration": 10, "teacher_action": "Taxminlarni eshitadi va yo‘naltiradi", "student_action": "Platformaga o‘z taxminini yozadi", "task": "Taxmin kiritish", "resource": "Algoritm laboratoriyasi", "product": "Bashorat ko‘rsatkichi"},
                    {"name": "Laboratoriyada tekshirish", "duration": 20, "teacher_action": "Tajriba ketma-ketligini nazorat qiladi", "student_action": "Parametrlarni o‘zgartirib qadamlarni kuzatadi", "task": "Qadamma-qadam ijro", "resource": "Simulyator", "product": "Haqiqiy olingan natija"},
                    {"name": "Xulosa va umumlashtirish", "duration": 10, "teacher_action": "Mantiqiy qoidani tizimlashtiradi", "student_action": "O‘z taxmini bilan natijani taqqoslaydi", "task": "Izoh yozish", "resource": "Portfolio", "product": "Yakuniy tushuntirish"}
                ]
            },
            {
                "title": "Juftlikda dasturlash (Pair Programming)",
                "slug": "juftlikda-dasturlash",
                "order": 3,
                "badge_color": "purple",
                "short_description": "Ikki o‘quvchi bitta kompyuterda birgalikda ishlaydi: biri kod yozuvchi ('Haydovchi - Driver'), ikkinchisi algoritmni tekshiruvchi va xatolarni aniqlovchi ('Navigator').",
                "applicable_when": "Murakkab algoritmlarni tuzishda xatolarni tez aniqlash va kompyuterlar soni cheklangan sharoitda o‘quvchilar hamkorligini kuchaytirish kerak bo‘lganda.",
                "teacher_role": "• Juftliklarni teng kuchli qilib shakllantiradi;\n• Rollar almashinishini (har 15 daqiqada) nazorat qiladi;\n• Kod sifatini birgalikda muhokama qiladi.",
                "student_role": "• 'Driver' sifatida kod kiritadi yoki bloklarni joylashtiradi;\n• 'Navigator' sifatida mantiqiy xatolarni ko‘rib boradi;\n• Rol almashib ikkala ko‘nikmani egallaydi.",
                "lesson_stages_overview": "1. Juftliklarni belgilash va brifing (5 daqiqa)\n2. 1-bosqich: A-haydovchi, B-navigator (15 daqiqa)\n3. Rollar almashinuvi: B-haydovchi, A-navigator (15 daqiqa)\n4. O‘zaro tekshiruv va refleksiya (10 daqiqa)",
                "sample_cs_case": "9-sinfda: Ikki sonning kattasini topuvchi va tarmoqlanuvchi shartli algoritmni juftlikda sinovdan o‘tkazish va tenglik holatidagi mantiqiy xatoni tuzatish.",
                "required_equipment": "Bitta kompyuterga 2 nafar o‘quvchi, juftlik kartochkalari.",
                "foreign_country": "Buyuk Britaniya (Angliya)",
                "foreign_practice_case": "Buyuk Britaniya Milliy Informatika Ta'limi Markazi (NCCE) va Raspberry Pi jamg‘armasi tomonidan tavsiya etilgan '12 Computing Pedagogy Principles' orasida juftlikda dasturlash rasmiy o‘qitish tamoyili sifatida belgilangan.",
                "source_citation": "National Centre for Computing Education (NCCE) - 12 Pedagogy Principles (rasmiy manba: teachcomputing.org)",
                "source_url": "https://teachcomputing.org/",
                "adaptation_recommendation": "Maktabda har bir o‘quvchiga alohida kompyuter yetishmaydigan sharoitda ushbu metod pedagogik kamchilikni metodik yutuqqa aylantiradi.",
                "default_stages_template": [
                    {"name": "Rollar taqsimoti va vazifa tushuntiruvi", "duration": 5, "teacher_action": "Driver va Navigator qoidalarini eslatadi", "student_action": "Rollarini kelishib oladilar", "task": "Juftlik shartnomasi", "resource": "Metod kartochkasi", "product": "Juftlik protokoli"},
                    {"name": "1-raund: Boshlang‘ich kodlash", "duration": 15, "teacher_action": "Navigator faolligini kuzatadi", "student_action": "Driver kod yozadi, Navigator xatoni tekshiradi", "task": "Boshlang‘ich algoritm", "resource": "Algoritmlar laboratoriyasi", "product": "Dastlabki kod"},
                    {"name": "Rollar almashinuvi (2-raund)", "duration": 15, "teacher_action": "Rollar almashganini tekshiradi", "student_action": "Driver va Navigator o‘rin almashadi", "task": "Optimizatsiya", "resource": "Simulyator", "product": "Yaxshilangan yechim"},
                    {"name": "O‘zaro taqriz va xulosa", "duration": 10, "teacher_action": "Juftliklarni umumiy muhokamaga tortadi", "student_action": "Bir-birining hissasini baholaydi", "task": "O‘zaro tahlil", "resource": "Portfolio", "product": "Jamoaviy hisobot"}
                ]
            },
            {
                "title": "Tadqiqot va tajriba orqali o‘rganish (Inquiry-Based Learning)",
                "slug": "tadqiqot-va-tajriba",
                "order": 4,
                "badge_color": "teal",
                "short_description": "O‘quvchilar mustaqil ravishda parametrlarni o‘zgartirib simulyatsiya o‘tkazadilar, olingan ma'lumotlarni tahlil qiladilar va xulosalarini isbotlaydilar.",
                "applicable_when": "Ma'lumotlar bilan ishlash, statistik tahlil va formulalarning real o‘zgarishlarga ta'sirini ko‘rgazmali tushunish kerak bo‘lganda.",
                "teacher_role": "• Tajriba parametrlarini va simulyatsiya muhitini taqdim etadi;\n• O‘quvchilarni ma'lumotlar tahliliga undaydi;\n• Gipoteza va olingan natija orasidagi farqni tahlil qildiradi.",
                "student_role": "• O‘zgaruvchilar qiymatini o‘zgartirib tajriba o‘tkazadi;\n• Grafiklarni tahlil qiladi;\n• Sabab-oqibat bog‘liqligini asoslaydi.",
                "lesson_stages_overview": "1. Tadqiqot savolini belgilash (5 daqiqa)\n2. Parametrlarni o‘zgartirish va tajriba (15 daqiqa)\n3. Diagramma va tahlil (15 daqiqa)\n4. Xulosa va tavsiyalar (10 daqiqa)",
                "sample_cs_case": "9-sinfda: 'Qurilmalarning ishlash vaqti 1 soatga qisqartirilsa, umumiy energiya sarfi necha foizga kamayadi?' savoli bo‘yicha diagramma tuzish va formulalar yordamida tekshirish.",
                "required_equipment": "Elektron jadvallar, Ma'lumotlar laboratoriyasi, grafik vositalari.",
                "foreign_country": "Buyuk Britaniya (Angliya)",
                "foreign_practice_case": "Buyuk Britaniya Ta'lim Departamenti (DfE) Milliy o‘quv dasturida 'Computing programmes of study (Key Stage 3-4)' hisoblash tafakkurini (computational thinking) rivojlantirish uchun simulyatsiya va ma'lumotlar tahlili orqali tadqiqot o‘tkazish asosiy talab sifatida belgilangan.",
                "source_citation": "UK Department for Education - National curriculum in England: computing programmes of study (rasmiy manba: gov.uk)",
                "source_url": "https://www.gov.uk/government/publications/national-curriculum-in-england-computing-programmes-of-study",
                "adaptation_recommendation": "Katta hajmdagi ma'lumotlar o‘rniga 5 kunlik maktab elektr sarfi kabi ko‘rgazmali va o‘quvchiga yaqin misollardan foydalaniladi.",
                "default_stages_template": [
                    {"name": "Tadqiqot gipotezasi", "duration": 5, "teacher_action": "Tadqiqot savolini e'lon qiladi", "student_action": "Gipotezani shakllantiradi", "task": "Gipoteza qaydi", "resource": "Ma'lumotlar laboratoriyasi", "product": "Gipoteza ko‘rsatkichi"},
                    {"name": "Ma'lumotlarni kiritish va tahrirlash", "duration": 15, "teacher_action": "O‘lchov birliklarini nazorat qiladi", "student_action": "Jadvalga qiymatlarni kiritadi va formulani tekshiradi", "task": "Jadval hisobi", "resource": "Kalkulyator", "product": "To‘ldirilgan jadval"},
                    {"name": "Grafik tahlil va ssenariy taqqoslash", "duration": 15, "teacher_action": "Diagramma turlarini tushuntiradi", "student_action": "Chart.js grafiklarini chizadi va sarfni taqqoslaydi", "task": "Vizualizatsiya", "resource": "Grafik muhiti", "product": "Qiyosiy diagramma"},
                    {"name": "Tadqiqot xulosasi", "duration": 10, "teacher_action": "Xulosalarni baholaydi", "student_action": "'Nima o‘zgardi va nima sababdan?' savoliga javob yozadi", "task": "Refleksiya", "resource": "Portfolio", "product": "Tadqiqot hisoboti"}
                ]
            },
            {
                "title": "Teskari sinf (Flipped Classroom)",
                "slug": "teskari-sinf",
                "order": 5,
                "badge_color": "indigo",
                "short_description": "O‘quvchi nazariy tushunchalarni darsdan oldin platformada mustaqil o‘rganadi, sinfda esa 45 daqiqaning barchasi qizg‘in amaliy mashg‘ulot va laboratoriyaga ajratiladi.",
                "applicable_when": "Nazariy tushunchalar ko‘p bo‘lib, dars vaqtida o‘qituvchi ma'ruzaga chalg‘imasdan 100% amaliy tajribaga e'tibor qaratishi kerak bo‘lganda.",
                "teacher_role": "• Darsdan oldin ko‘rsatmalarni joylashtiradi;\n• Sinfda individual qiyinchilikka uchragan o‘quvchilarga yordam beradi;\n• Amaliy laboratoriyani boshqaradi.",
                "student_role": "• Uyda dars materialini o‘rganib keladi;\n• Sinfda to‘g‘ridan-to‘g‘ri amaliy loyiha va simulyatsiya bilan shug‘ullanadi;\n• Savollari bo‘yicha o‘qituvchidan maslahat oladi.",
                "lesson_stages_overview": "1. Darsdan oldingi bilimlarni tekshirish (5 daqiqa)\n2. Amaliy laboratoriya vazifasi (25 daqiqa)\n3. Yakuniy mahsulotni topshirish (10 daqiqa)\n4. Xulosa (5 daqiqa)",
                "sample_cs_case": "9-sinfda: 'Energiya sarfi formulasi va o‘lchov birliklari' bilan mustaqil tanishib kelib, sinfda to‘liq amaliy simulyatsiya va tejash algoritmini tuzish.",
                "required_equipment": "Platformaga kirish imkoni, kompyuter sinfi.",
                "foreign_country": "Estoniya",
                "foreign_practice_case": "Estoniyaning raqamli ta'lim ekotizimida (e-School va Opiq darsliklar tarmog‘i) nazariya o‘quvchilar tomonidan mustaqil o‘zlashtirilib, dars vaqti faqat ijodiy laboratoriya va muammoli munozaralarga sarflanadi.",
                "source_citation": "e-Estonia Briefing Centre & Haridus- ja Teadusministeerium (Estoniya Ta'lim Vazirligi - hm.ee)",
                "source_url": "https://educationendowmentfoundation.org.uk/education-evidence/teaching-learning-toolkit/flipped-learning",
                "adaptation_recommendation": "Internet yetarli bo‘lmagan maktablarda o‘quvchilarga qisqa matnli ko‘rsatmalar avvaldan beriladi, sinfda esa kompyuterlar to‘liq laboratoriya uchun ishlatiladi.",
                "default_stages_template": [
                    {"name": "Tezkor savol-javob (Darsdan oldingi bilimlar)", "duration": 5, "teacher_action": "Asosiy tushunchalarni aniqlashtiradi", "student_action": "O‘zlashtirgan tushunchalarini aytadi", "task": "Tezkor sinov", "resource": "Platforma", "product": "Faollik qaydi"},
                    {"name": "Amaliy laboratoriya tajribasi", "duration": 25, "teacher_action": "Individual yo‘l-yo‘riq beradi", "student_action": "Laboratoriyada mustaqil tajriba qiladi", "task": "Tajriba o‘tkazish", "resource": "Interaktiv laboratoriya", "product": "Laboratoriya hisobi"},
                    {"name": "Mahsulotni rasmiylashtirish va topshirish", "duration": 10, "teacher_action": "Birinchi versiyalarni ko‘radi", "student_action": "Ishini portfolioga yuklaydi", "task": "Topshirish", "resource": "Portfolio", "product": "Dastlabki mahsulot"},
                    {"name": "Takomillashtirish yo‘nalishlari", "duration": 5, "teacher_action": "Keyingi qadamlarni belgilaydi", "student_action": "O‘z rejasini tuzadi", "task": "Reja", "resource": "Daftar/Tizim", "product": "Takomillashtirish rejasi"}
                ]
            }
        ]

        created_methods = []
        for m_data in methods_data:
            method, _ = TeachingMethod.objects.update_or_create(
                slug=m_data['slug'],
                defaults=m_data
            )
            created_methods.append(method)

        # 4. Namunaviy Loyiha shablonlari (7 ta to'liq 4 darslik loyiha)
        all_projects_data = [
            {
                "slug": "elektr-energiyasidan-oqilona-foydalanish",
                "title": "Maktabda elektr energiyasidan oqilona foydalanish",
                "topic": "Informatika va ma'lumotlar tahlili yordamida resurslarni tejash",
                "description": "Ushbu 4 darslik kompleks loyihada 9-sinf o‘quvchilari maktab elektr jihozlari sarfini o‘rganadilar, jadvallar va diagrammalar tuzadilar, avtomatlashtirilgan tejash algoritmini modellashtiradilar hamda maktab ma'muriyati uchun aniq takliflar to‘plamini shakllantiradilar.",
                "steps": [
                    {
                        "lesson_number": 1,
                        "title": "1-dars: Muammo, ma’lumotlar va taxmin",
                        "instructions": "Maktabda qaysi qurilmalar eng ko‘p elektr energiyasini sarflaydi? Boshlang‘ich ma'lumotlarni aniqlang va tejash imkoniyatlari bo‘yicha gipoteza (taxmin) ilgari suring.",
                        "task_details": "Maktabdagi 5 xil qurilma (kompyuterlar, chiroqlar, proyektor, konditsioner va b.) ro‘yxatini tuzing, ularning quvvatini aniqlang va qaysi biri eng ko‘p sarf qilishini taxmin qiling.",
                        "expected_artifact": "Muammo bayoni va boshlang‘ich gipoteza (taxmin matni)",
                        "recommended_lab": "data"
                    },
                    {
                        "lesson_number": 2,
                        "title": "2-dars: Hisoblash, jadval va diagramma",
                        "instructions": "Formula yordamida har bir qurilmaning kunlik va haftalik energiya sarfini (kWh) hisoblang. Olingan ma'lumotlar asosida ko‘rgazmali diagramma chizing.",
                        "task_details": "Ma'lumotlar laboratoriyasida 5 kunlik jadvalni to‘ldiring: Energiya = Quvvat × Vaqt × Soni / 1000 formulasini qo‘llang va Chart.js diagrammasini shakllantiring.",
                        "expected_artifact": "Elektr sarfi hisob-kitob jadvali va qiyosiy diagramma",
                        "recommended_lab": "data"
                    },
                    {
                        "lesson_number": 3,
                        "title": "3-dars: Ma'lumotlar tahlili va tejash ssenariysi",
                        "instructions": "Agar qurilmalarning keraksiz ishlash vaqti qisqartirilsa, umumiy sarf qanchaga kamayadi? Ma'lumotlar laboratoriyasida tejash ssenariysini modellashtiring va foiz hisobini bajaring.",
                        "task_details": "Ma'lumotlar laboratoriyasida (Maktab elektr energiyasi sarfi) tejash ssenariysi slayderi yordamida ishlash vaqtini qisqartiring va sarfning kamayishini modellashtiring. Nazorat misoli orqali (100W × 5h × 2 ta = 1.0 kWh sarfni 1 soat qisqartirib 0.8 kWh ga tushirish — 20% tejash) olingan natijani tahlil qiling va tejamkorlik xulosasini taqdim eting.",
                        "expected_artifact": "Tejash ssenariysi hisob-kitobi va energiya tejash rejasi",
                        "recommended_lab": "data"
                    },
                    {
                        "lesson_number": 4,
                        "title": "4-dars: Tavsiya, taqdimot va takomillashtirish",
                        "instructions": "O‘qituvchi tavsiyasi asosida loyihangizdagi kamchiliklarni to‘g‘rilang, yangi versiyani tayyorlang va maktab rahbariyati uchun yakuniy taqdimot hamda refleksiyani yozing.",
                        "task_details": "Barcha 3 ta dars natijalarini umumlashtiring. O‘qituvchi bergan izoh asosida xatolarni bartaraf eting va 3 ta refleksiya savoliga javob bering.",
                        "expected_artifact": "Maktab ma'muriyatiga yakuniy taqdimot xulosasi va o‘quvchi refleksiyasi",
                        "recommended_lab": "data"
                    }
                ]
            },
            {
                "slug": "smart-school-scratch-loyihasi",
                "title": "Smart School: Scratch orqali interaktiv ta’limiy o‘yin yaratish",
                "topic": "Blokli vizual dasturlash, qalam va animatsiyalar",
                "description": "Ushbu 4 darslik ijodiy loyihada o‘quvchilar Scratch laboratoriyasida bloklar yordamida geometrik shakllar, harakatlanuvchi spraitlar va ta’limiy savol-javob o‘yinini loyihalaydilar.",
                "steps": [
                    {
                        "lesson_number": 1,
                        "title": "1-dars: O‘yin ssenariysi, spraitlar va gipoteza",
                        "instructions": "O‘yin maqsadini belgilang: qahramon qanday harakat qiladi va qanday to‘siqlarga duch keladi? Boshlang‘ich loyiha rejasini tuzing.",
                        "task_details": "Scratch laboratoriyasida sprait koordinatalarini (x, y) aniqlang va boshlang‘ich dialog bloklarini rejalashtiring.",
                        "expected_artifact": "O‘yin ssenariysi va bloklar rejasi",
                        "recommended_lab": "scratch"
                    },
                    {
                        "lesson_number": 2,
                        "title": "2-dars: Qahramon harakati, sikllar va geometriya",
                        "instructions": "Mushukcha yoki qahramon harakatini sikl (takrorlash) bloklari orqali modellashtiring. Qalam bilan maydonga geometrik to‘siqlar chizing.",
                        "task_details": "Scratch laboratoriyasida 6 marta takrorlash (oltiburchak) yoki kvadrat chizish algoritmini amalda ishga tushiring.",
                        "expected_artifact": "Harakatlanuvchi sprait va geometrik chizma skripti",
                        "recommended_lab": "scratch"
                    },
                    {
                        "lesson_number": 3,
                        "title": "3-dars: To‘siqlar, hisoblagich va tovush effektlari",
                        "instructions": "Devordan qaytish (bounce) va tovush effektlarini qo‘shing. O‘yindagi ballar va xabarlarni sozlang.",
                        "task_details": "Chegaraga yetganda qaytish va say_text bloklari bilan to‘liq interaktivlik yarating.",
                        "expected_artifact": "Interaktiv o‘yin prototipi",
                        "recommended_lab": "scratch"
                    },
                    {
                        "lesson_number": 4,
                        "title": "4-dars: O‘yinni testlash, takomillashtirish va taqdimot",
                        "instructions": "O‘qituvchi va sinfdoshlar fikri asosida xatolarni to‘g‘rilang va yakuniy o‘yin loyihasini taqdim eting.",
                        "task_details": "Yaratilgan o‘yin bo‘yicha tahliliy hisobot va o‘quvchi refleksiyasini tayyorlang.",
                        "expected_artifact": "Yakuniy Scratch o‘yini loyihasi va refleksiya",
                        "recommended_lab": "scratch"
                    }
                ]
            },
            {
                "slug": "kiberxavfsizlik-va-axborot-himoyasi",
                "title": "Maktab axborot tizimini kiberhujumlardan himoyalash",
                "topic": "Axborot xavfsizligi, shifrlash va parollar mustahkamligi",
                "description": "9-sinf o‘quvchilari maktab elektron kundaligi va o‘qituvchilar kabineti xavfsizligini ta’minlash uchun Sezar shifri, binar XOR va xavfsiz parollar protokolini ishlab chiqadilar.",
                "steps": [
                    {
                        "lesson_number": 1,
                        "title": "1-dars: Zaif parollar va kiberxavfsizlik xatarlari",
                        "instructions": "Maktab o‘quvchilari qo‘llaydigan sodda parollar nima uchun xavfli? Kiberxavfsizlik muammosini o‘rganing.",
                        "task_details": "Kriptografiya laboratoriyasida '123456', 'admin', 'Parol123' kabi parollarning buzilish vaqtini tahlil qiling.",
                        "expected_artifact": "Zaif parollar xavfi bo‘yicha tahliliy hisobot",
                        "recommended_lab": "crypto"
                    },
                    {
                        "lesson_number": 2,
                        "title": "2-dars: Sezar va XOR shifrlash algoritmlari tajribasi",
                        "instructions": "Simmetrik shifrlash usullarini amalda sinang: Sezar siljish kaliti va binar XOR amali.",
                        "task_details": "Kriptografiya laboratoriyasida maktab nomini K=3 kalit bilan shifrlang va binar bitlar o‘zgarishini qayd eting.",
                        "expected_artifact": "Shifrlash jadvallari va binar hisob-kitoblar",
                        "recommended_lab": "crypto"
                    },
                    {
                        "lesson_number": 3,
                        "title": "3-dars: Parollar entropiyasini 70+ bitga yetkazish",
                        "instructions": "Superkompyuterlar ham buza olmaydigan (300+ yil) mustahkam parollar yaratish qoidalarini ishlab chiqing.",
                        "task_details": "Katta/kichik harflar, sonlar va belgilarni birlashtirib 80+ bit entropiyali xavfsiz parol modelini yarating.",
                        "expected_artifact": "Kiberhimoyalangan parollar namunasi va entropiya hisobi",
                        "recommended_lab": "crypto"
                    },
                    {
                        "lesson_number": 4,
                        "title": "4-dars: Maktab kiberxavfsizlik reglamenti va himoya",
                        "instructions": "Barcha o‘quvchilar va o‘qituvchilar uchun kiberxavfsizlik yo‘riqnomasini rasmiylashtiring.",
                        "task_details": "O‘qituvchi taklifi asosida tavsiyalarni to‘ldirib, yakuniy xavfsizlik protokolini topshiring.",
                        "expected_artifact": "Maktab axborot xavfsizligi reglamenti va refleksiya",
                        "recommended_lab": "crypto"
                    }
                ]
            },
            {
                "slug": "kompyuter-tarmogini-loyihalash",
                "title": "Kompyuter sinfi lokal tarmog‘ini loyihalash va marshrutlash",
                "topic": "Kompyuter tarmoqlari, topologiyalar va IPv4 subnetting",
                "description": "Maktabning yangi kompyuter sinfi uchun eng ishonchli tarmoq topologiyasini tanlash, kabel uzilishiga chidamlilikni tekshirish va IP-manzillarni to‘g‘ri taqsimlash loyihasi.",
                "steps": [
                    {
                        "lesson_number": 1,
                        "title": "1-dars: Tarmoq ehtiyojlari va gipoteza",
                        "instructions": "12 ta o‘quvchi kompyuteri va 1 ta o‘qituvchi serveri uchun qaysi topologiya eng qulay? Boshlang‘ich gipotezani belgilang.",
                        "task_details": "Yulduz (Star), Shina (Bus) va Halqa (Ring) topologiyalarining afzallik va kamchiliklarini yozing.",
                        "expected_artifact": "Tarmoq loyihasi talablari va gipoteza",
                        "recommended_lab": "network"
                    },
                    {
                        "lesson_number": 2,
                        "title": "2-dars: Topologiya simulyatsiyasi va avariya sinovi",
                        "instructions": "Tarmoq laboratoriyasida kabel uzilishini sinab ko‘ring: Yulduzda kabel uzilsa nima bo‘ladi, shinada nima bo‘ladi?",
                        "task_details": "Ping yuboring va bitta kabel uzilganda paket yetkazilishi saqlanib qolishini amalda tekshiring.",
                        "expected_artifact": "Avariya sinovi protokoli va ishonchlilik xulosasi",
                        "recommended_lab": "network"
                    },
                    {
                        "lesson_number": 3,
                        "title": "3-dars: IPv4 /24 qism-tarmoqlarini rejalashtirish",
                        "instructions": "Sinf kompyuterlari uchun IP-manzillar jadvalini tuzing: Network ID, Broadcast va birinchi/oxirgi IP-lar.",
                        "task_details": "Tarmoq kalkulyatorida 192.168.1.0/24 tarmog‘ini hisoblab, har bir kompyuterga unikal IP biriktiring.",
                        "expected_artifact": "IP-manzillash jadvali va subnetting hisobi",
                        "recommended_lab": "network"
                    },
                    {
                        "lesson_number": 4,
                        "title": "4-dars: Maktab tarmog‘i xaritasi va yakuniy taqdimot",
                        "instructions": "Loyiha chizmasini yakunlang va tarmoq ma’muri uchun foydalanish yo‘riqnomasini topshiring.",
                        "task_details": "O‘qituvchi fikrlari asosida IP-sxemani mukammallashtirib, yakuniy taqdimotni tayyorlang.",
                        "expected_artifact": "Lokal tarmoq sxemasi va o‘quvchi refleksiyasi",
                        "recommended_lab": "network"
                    }
                ]
            },
            {
                "slug": "kutubxona-qidiruv-va-saralash",
                "title": "Kutubxona kitoblarini tezkor qidirish va saralash tizimi",
                "topic": "Algoritmlar samaradorligi, Bubble sort va Binary search",
                "description": "Maktab kutubxonasidagi 1000 ta kitob ichidan kerakli kitobni eng kam vaqtda topish uchun saralash algoritmlarini taqqoslash va ikkilik qidiruv tizimini modellashtirish.",
                "steps": [
                    {
                        "lesson_number": 1,
                        "title": "1-dars: Tartibsiz ma’lumotlar va qidiruv muammosi",
                        "instructions": "Tartiblanmagan ro‘yxatda bitta kitobni topish uchun necha marta tekshirish kerak? Muammoni tahlil qiling.",
                        "task_details": "Chiziqli qidiruv vaqtini baholang va gipotezani shakllantiring.",
                        "expected_artifact": "Muammo bayoni va qidiruv gipotezasi",
                        "recommended_lab": "sorting"
                    },
                    {
                        "lesson_number": 2,
                        "title": "2-dars: Pufaksimon va Tanlash saralash tahlili",
                        "instructions": "Saralash laboratoriyasida pufaksimon va tanlash algoritmlarining qadamlarini kuzating.",
                        "task_details": "Taqqoslashlar soni va almashtirishlar (swaps) hisobini yozib oling.",
                        "expected_artifact": "Saralash algoritmlari taqqoslash jadvali",
                        "recommended_lab": "sorting"
                    },
                    {
                        "lesson_number": 3,
                        "title": "3-dars: Ikkilik qidiruv (Binary Search) tezligi",
                        "instructions": "Saralangan massivda ikkilik qidiruv qanchalik tez ishlashini amalda tekshiring: O(log N) samaradorligi.",
                        "task_details": "Saralash laboratoriyasida ikkilik qidiruvni ishga tushirib, 2-3 qadamda sonni topishni qayd eting.",
                        "expected_artifact": "Ikkilik qidiruv sinov natijalari",
                        "recommended_lab": "sorting"
                    },
                    {
                        "lesson_number": 4,
                        "title": "4-dars: Algoritmlar samaradorligi hisoboti",
                        "instructions": "O‘qituvchi tavsiyasi asosida algoritmlarning tezlik ko‘rsatkichlarini solishtiring va kutubxona uchun tavsiya bering.",
                        "task_details": "Yakuniy xulosalar va o‘quvchi refleksiyasini portfolioga topshiring.",
                        "expected_artifact": "Algoritmlar samaradorligi hisoboti va refleksiya",
                        "recommended_lab": "sorting"
                    }
                ]
            },
            {
                "slug": "ikkilik-kalkulyator-va-mantiqiy-sxemalar",
                "title": "Ikkilik kalkulyator va mantiqiy sxemalar modeli",
                "topic": "Mantiqiy amallar, rostlik jadvallari va Half-Adder",
                "description": "Kompyuter protsessori (ALU) sonlarni qanday qo‘shishini tushunish uchun AND, OR, XOR ventillaridan foydalanib 1-bitli ikkilik jamlagich (Half-Adder) modelini yaratish.",
                "steps": [
                    {
                        "lesson_number": 1,
                        "title": "1-dars: Mantiqiy rostlik qonuniyatlari va gipoteza",
                        "instructions": "Kompyuter faqat 0 va 1 signallarini tushunadi. Mantiqiy ventillar orqali qanday hisob-kitob qilish mumkin?",
                        "task_details": "Mantiqiy laboratoriyada AND, OR, NOT ventillarining rostlik jadvallarini tekshiring.",
                        "expected_artifact": "Rostlik jadvallari tahlili va gipoteza",
                        "recommended_lab": "logic"
                    },
                    {
                        "lesson_number": 2,
                        "title": "2-dars: XOR ventili va ikkilik qo‘shish mantiqi",
                        "instructions": "Ikkilik qo‘shish qoidasini o‘rganing: 0+0=0, 0+1=1, 1+0=1, 1+1=10 (o‘nlikda 2).",
                        "task_details": "XOR ventili nima uchun qo‘shishning birinchi razryadi (Sum) bo‘lishini amalda isbotlang.",
                        "expected_artifact": "Ikkilik qo‘shish jadvali va tahlil",
                        "recommended_lab": "logic"
                    },
                    {
                        "lesson_number": 3,
                        "title": "3-dars: 1-bitli Half-Adder (Jamlagich) sxemasini yig‘ish",
                        "instructions": "Mantiqiy laboratoriyada Half-Adder modelini ishga tushiring: Sum (XOR) va Carry (AND) chiqishlarini kuzating.",
                        "task_details": "1+1 kiritilganda chiroqlar qanday yonishini va ikkilik 10 natijasi chiqishini qayd eting.",
                        "expected_artifact": "Half-Adder sxemasi sinov hisoboti",
                        "recommended_lab": "logic"
                    },
                    {
                        "lesson_number": 4,
                        "title": "4-dars: Protsessor ALU qismi tahlili va taqdimot",
                        "instructions": "O‘qituvchi fikrlari asosida mantiqiy sxemaning ishlashini to‘liq ta’riflang va xulosangizni yozing.",
                        "task_details": "Yakuniy mantiqiy model hisoboti va o‘quvchi refleksiyasini topshiring.",
                        "expected_artifact": "Protsessor mikrosxemasi modeli hisoboti va refleksiya",
                        "recommended_lab": "logic"
                    }
                ]
            },
            {
                "slug": "python-baholash-dasturi",
                "title": "Python tilida avtomatlashtirilgan baholash dasturi",
                "topic": "Matnli dasturlash: shartlar, sikllar va ro‘yxatlar",
                "description": "O‘quvchilar ballarini avtomatik tahlil qiluvchi, o‘rtacha ballni hisoblovchi va rag‘batlantirish tavsiyasini chiqaruvchi haqiqiy Python dasturini ishlab chiqish.",
                "steps": [
                    {
                        "lesson_number": 1,
                        "title": "1-dars: Dastur talablari va algoritm loyihasi",
                        "instructions": "O‘qituvchi 30 ta o‘quvchining ballarini tezkor hisoblashi uchun dastur qanday ishlashi kerak? Reja tuzing.",
                        "task_details": "Python terminalida o‘zgaruvchilar va print() funksiyasini sinab, boshlang‘ich kod skeletini yozing.",
                        "expected_artifact": "Dastur spetsifikatsiyasi va gipoteza",
                        "recommended_lab": "python"
                    },
                    {
                        "lesson_number": 2,
                        "title": "2-dars: if/elif/else yordamida baholash mezonlari",
                        "instructions": "Ball 85 dan yuqori bo‘lsa 'A'lo', 70 dan yuqori bo‘lsa 'Yaxshi' deb chiqaruvchi shartli mantiqni dasturlang.",
                        "task_details": "Python laboratoriyasida shart operatorlarini turli qiymatlar bilan sinovdan o‘tkazing.",
                        "expected_artifact": "Shartli baholash Python kodi",
                        "recommended_lab": "python"
                    },
                    {
                        "lesson_number": 3,
                        "title": "3-dars: Ro‘yxatlar (list) va sikllar bilan statistik tahlil",
                        "instructions": "Sinfdagi barcha ballarni bitta ro‘yxatda saqlang va sum(), len(), max(), min() orqali tahlil qiling.",
                        "task_details": "Python terminalida 7 ta o‘quvchi bali bo‘yicha o‘rtacha ko‘rsatkichni hisoblab chiqaring.",
                        "expected_artifact": "Statistik tahlil dasturi skripti",
                        "recommended_lab": "python"
                    },
                    {
                        "lesson_number": 4,
                        "title": "4-dars: Dastur testlari, takomillashtirish va refleksiya",
                        "instructions": "O‘qituvchi izohlari asosida dasturdagi xatolarni to‘g‘rilang va foydalanuvchi qo‘llanmasini yozing.",
                        "task_details": "Yakuniy Python skripti (.py) va o‘quvchi refleksiyasini portfolioga yuklang.",
                        "expected_artifact": "Yakuniy Python dasturi va o‘quvchi refleksiyasi",
                        "recommended_lab": "python"
                    }
                ]
            }
        ]

        created_projects = []
        for p_data in all_projects_data:
            steps_list = p_data.pop("steps")
            proj_obj, _ = ProjectTemplate.objects.update_or_create(
                slug=p_data["slug"],
                defaults={
                    "title": p_data["title"],
                    "topic": p_data["topic"],
                    "description": p_data["description"],
                    "grade": 9,
                    "total_lessons": 4,
                    "is_active": True
                }
            )
            for s_info in steps_list:
                ProjectLessonStep.objects.update_or_create(
                    project_template=proj_obj,
                    lesson_number=s_info["lesson_number"],
                    defaults=s_info
                )

            # 9-A sinfiga biriktirish
            asg, _ = ClassProjectAssignment.objects.get_or_create(
                project_template=proj_obj,
                classroom=class_9a,
                defaults={
                    "teacher": teacher_user,
                    "is_group_project": True,
                    "deadline": "2026-12-25"
                }
            )
            created_projects.append(proj_obj)

        project_tmpl = created_projects[0]
        assignment = ClassProjectAssignment.objects.filter(project_template=project_tmpl, classroom=class_9a).first()

        # 6. Guruh yaratish: "Eko-Informatiklar guruhi"
        group, _ = ProjectGroup.objects.get_or_create(
            assignment=assignment,
            name="Eko-Informatiklar guruhi",
            defaults={
                'leader': student1,
                'role_distribution': "1. Anvar Saidov - Ma'lumotlar yig'ish, texnik hisob-kitob va algoritm sinovi\n2. Madina Alimova - Jadval va diagramma vizualizatsiyasi, taqdimot tayyorlash"
            }
        )
        group.members.set([student1, student2])
        group.save()

        # 7. O‘qituvchi darsi namunasi (Dars konstruktori orqali)
        pbl_method = created_methods[0]
        sample_lesson, _ = LessonPlan.objects.get_or_create(
            title="Maktabda elektr energiyasidan oqilona foydalanish tahlili",
            teacher=teacher_user,
            defaults={
                'classroom': class_9a,
                'method': pbl_method,
                'target_grade': 9,
                'learning_objective': "O‘quvchi tarmoqlanuvchi algoritmlar va jadvallar yordamida maktab elektr energiyasi sarfini hisoblaydi, tejash ssenariysini modellashtiradi va o‘qituvchi izohidan so‘ng loyihani takomillashtiradi.",
                'duration_minutes': 45,
                'available_equipment': "Kompyuter sinfi (12 ta kompyuter), lokal tarmoq, proyektor, InformatikaLab platformasi",
                'activity_type': 'group',
                'status': 'assigned'
            }
        )
        if sample_lesson.stages.count() == 0:
            stages_init = [
                {"order": 1, "name": "Muammoli savol va kirish", "duration": 5, "teacher_action": "Maktab hisoblagichidagi yuqori sarf muammosini qo‘yadi", "student_action": "Muammoni guruhda muhokama qiladi", "task": "Gipoteza ilgari surish", "resources": "InformatikaLab", "expected_product": "Boshlang‘ich taxmin"},
                {"order": 2, "name": "Ma'lumotlar jadvali va formulalarni hisoblash", "duration": 15, "teacher_action": "Quvvat, vaqt va sarf formulalarini eslatadi", "student_action": "Ma'lumotlar laboratoriyasida 5 kunlik jadvalni to‘ldiradi", "task": "Energiya (kWh) hisobi", "resources": "Ma'lumotlar laboratoriyasi", "expected_product": "Jadval va Chart.js grafigi"},
                {"order": 3, "name": "Algoritm va tejash ssenariysi", "duration": 15, "teacher_action": "Tejash foizi hisoblashni kuzatadi", "student_action": "Algoritm laboratoriyasida shartli operatorlarni sinaydi", "task": "Tejash ssenariysi", "resources": "Algoritm laboratoriyasi", "expected_product": "Tejash hisoboti"},
                {"order": 4, "name": "Refleksiya va xulosalarni topshirish", "duration": 10, "teacher_action": "O‘quvchilar ishiga oraliq tavsiyalar beradi", "student_action": "Natijalarni portfolioga yuklaydi va refleksiya yozadi", "task": "Portfolioga topshirish", "resources": "Portfolio", "expected_product": "Dastlabki versiya (v1)"},
            ]
            for st in stages_init:
                LessonStage.objects.create(
                    lesson=sample_lesson,
                    order=st['order'],
                    name=st['name'],
                    duration_minutes=st['duration'],
                    teacher_action=st['teacher_action'],
                    student_action=st['student_action'],
                    task_description=st['task'],
                    resources=st['resources'],
                    expected_product=st['expected_product']
                )

        # 8. Namunaviy topshiriq va Versiyalar evolyutsiyasi (v1 -> o'qituvchi izohi -> v2)
        step1 = project_tmpl.steps.filter(lesson_number=1).first()
        if step1:
            submission, _ = ProjectSubmission.objects.get_or_create(
                assignment=assignment,
                lesson_step=step1,
                student=student1,
                defaults={
                    'group': group,
                    'status': 'resubmitted'
                }
            )

            # Versiya 1 (Dastlabki variant)
            v1, _ = SubmissionVersion.objects.get_or_create(
                submission=submission,
                version_number=1,
                defaults={
                    'title': "1-dars dastlabki mahsuloti: Elektr sarfi gipotezasi",
                    'content_text': "Bizning guruhimiz maktabdagi kompyuter xonasi va yo‘laklardagi chiroqlarni o‘rgandi. Bizning taxminimizcha, eng ko‘p elektr energiyasini kompyuterlar sarflaydi, chunki ular kuniga 5 soatdan ko‘p ishlaydi. Biroq formuladagi o‘lchov birliklari bo‘yicha biroz ikkilanmoqdamiz.",
                    'student_notes': "Dastlabki hisob-kitoblarimiz xomaki holatda.",
                    'individual_contribution': "Anvar Saidov: Kompyuterlarning quvvat pasportlarini ko‘rib chiqdi (har biri 150W).",
                    'is_draft': False
                }
            )

            # O'qituvchi izohi (v1 uchun)
            if v1.feedbacks.count() == 0:
                TeacherFeedback.objects.create(
                    version=v1,
                    teacher=teacher_user,
                    feedback_text="Gipoteza juda to‘g‘ri qo‘yilgan! Biroq quvvatni (W) vaqtga (soat) ko‘paytirgandan so‘ng albatta 1000 ga bo‘lib, energiya o‘lchov birligini kilovatt-soatda (kWh) ifodalang. Hisob-kitobingizni aniqlashtirib, yangi versiya topshiring.",
                    requires_revision=True,
                    criteria_clarity="Yaxshi",
                    criteria_technical="Kichik xatolik bor",
                    criteria_creativity="Ijodiy va chuqur"
                )

            # Versiya 2 (Tuzatilgan va takomillashtirilgan variant)
            v2, _ = SubmissionVersion.objects.get_or_create(
                submission=submission,
                version_number=2,
                defaults={
                    'title': "1-dars takomillashtirilgan mahsuloti: To‘liq hisoblangan gipoteza",
                    'content_text': "O‘qituvchimizning tavsiyasidan so‘ng formulani to‘g‘riladik: Energiya = Quvvat (150 W) × 5 soat × 12 dona kompyuter / 1000 = 9.0 kWh. Yo‘lak chiroqlari esa 100 W × 6 soat × 8 dona / 1000 = 4.8 kWh sarflaydi. Gipotezamiz matematik jihatdan to‘liq isbotlandi: kompyuter xonasi chiroqlardan qariyb 2 baravar ko‘p energiya sarflar ekan.",
                    'student_notes': "O‘qituvchi tavsiyasi asosida birliklar kWh ga o‘tkazildi va hisob aniqlandi.",
                    'individual_contribution': "Anvar Saidov: Formulani 1000 ga bo‘lib kWh ko‘rsatkichlarini hisoblab chiqdi.",
                    'is_draft': False
                }
            )

            # Yakuniy Refleksiya
            StudentReflection.objects.get_or_create(
                submission=submission,
                student=student1,
                defaults={
                    'what_created': "Maktab kompyuter xonasi va yoritish tizimining 1 kunlik energiya sarfini hisoblab, gipotezamizni isbotlagan hisobot yaratdim.",
                    'what_error_found': "Dastlabki versiyada quvvatni 1000 ga bo‘lishni unutgan edim va natija Watt-soatda chiqib, haddan tashqari katta ko‘ringan edi.",
                    'how_improved': "O‘qituvchimning izohidan so‘ng o‘lchov birligini kilovatt-soatga (kWh) o‘tkazdim va har bir qurilmaning aniq ulushini taqqosladim."
                }
            )

        self.stdout.write(self.style.SUCCESS("Barcha namunaviy ma'lumotlar muvaffaqiyatli yaratildi va bazaga yuklandi!"))
        self.stdout.write("Test hisoblari (login / parol):")
        self.stdout.write("  Administrator: admin / admin123")
        self.stdout.write("  O‘qituvchi (Jasur Karimov): oqituvchi / oqituvchi123")
        self.stdout.write("  O‘qituvchi (Malika Akbarova): malika_oqituvchi / oqituvchi123")
        self.stdout.write("  O‘quvchi (Anvar Saidov): oquvchi1 / oquvchi123")
        self.stdout.write("  O‘quvchi (Madina Alimova): oquvchi2 / oquvchi123")
        self.stdout.write("  O‘quvchi (Nodirbek Zokirov): nodir / oquvchi123")
        self.stdout.write("  O‘quvchi (Dilnoza Rahimova): dilnoza / oquvchi123")
