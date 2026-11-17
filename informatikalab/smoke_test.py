import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from accounts.models import User

client = Client()

print("==================================================")
print("INFORMATIKALAB SAHIFALARINI TEKSHIRISH (SMOKE TEST)")
print("==================================================")

# 1. Anonim foydalanuvchi
endpoints_anon = [
    ('/', 'Bosh sahifa'),
    ('/accounts/login/', 'Login sahifasi'),
]
for url, name in endpoints_anon:
    resp = client.get(url)
    print(f"[{resp.status_code}] {name:30} -> {url}")
    assert resp.status_code in [200, 302], f"Xatolik: {url} -> {resp.status_code}"

# 2. O'qituvchi sifatida kirish
teacher = User.objects.get(username='oqituvchi')
client.force_login(teacher)
print("\n--- O‘QITUVCHI TESTI (Jasur Karimov) ---")

endpoints_teacher = [
    ('/', 'O‘qituvchi Bosh sahifasi'),
    ('/methods/', 'Metodlar kutubxonasi'),
    ('/methods/loyiha-asosida-oqitish/', 'Metod: PBL kartochkasi'),
    ('/methods/muammoli-talim/', 'Metod: Muammoli ta’lim'),
    ('/methods/juftlikda-dasturlash/', 'Metod: Juftlikda dasturlash'),
    ('/methods/tadqiqot-va-tajriba/', 'Metod: Tadqiqot va tajriba'),
    ('/methods/teskari-sinf/', 'Metod: Teskari sinf'),
    ('/lessons/', 'Darslarim ro‘yxati'),
    ('/lessons/create/', 'Dars konstruktori'),
    ('/lessons/1/', 'Dars tafsiloti'),
    ('/lessons/1/print/', 'Dars chop etish ko‘rinishi'),
    ('/labs/', 'Laboratoriyalar bosh sahifasi'),
    ('/labs/algorithms/', 'Algoritmlar laboratoriyasi'),
    ('/labs/data/', 'Ma’lumotlar laboratoriyasi'),
    ('/labs/scratch/', 'Scratch vizual dasturlash laboratoriyasi'),
    ('/labs/crypto/', 'Kriptografiya laboratoriyasi'),
    ('/labs/network/', 'Kompyuter tarmoqlari laboratoriyasi'),
    ('/labs/sorting/', 'Saralash algoritmlari laboratoriyasi'),
    ('/labs/logic/', 'Mantiqiy sxemalar laboratoriyasi'),
    ('/labs/python/', 'Python dasturlash laboratoriyasi'),
    ('/projects/', 'Loyihalar ustaxonasi'),
    ('/projects/1/', 'Elektr energiyasi namunaviy loyiha'),
    ('/projects/assignment/1/', 'Sinf loyihasi maydoni'),
    ('/portfolio/', 'O‘qituvchi tekshiruv paneli'),
    ('/accounts/profile/', 'O‘qituvchi profili va sozlamalari'),
    ('/accounts/classrooms/', 'Sinflar ro‘yxati'),
    ('/accounts/classrooms/1/', '9-A sinf boshqaruvi'),
]

for url, name in endpoints_teacher:
    resp = client.get(url)
    print(f"[{resp.status_code}] {name:35} -> {url}")
    assert resp.status_code == 200, f"Xatolik: {name} ({url}) -> {resp.status_code}"

# 3. O'quvchi sifatida kirish
student = User.objects.get(username='oquvchi1')
client.force_login(student)
print("\n--- O‘QUVCHI TESTI (Anvar Saidov) ---")

endpoints_student = [
    ('/', 'O‘quvchi Bosh sahifasi'),
    ('/lessons/student/', 'O‘quvchiga biriktirilgan darslar'),
    ('/lessons/1/', 'O‘quvchi dars jarayonini ko‘rishi'),
    ('/labs/', 'Laboratoriyalar'),
    ('/labs/algorithms/', 'Algoritmlar simulyatori'),
    ('/labs/data/', 'Ma’lumotlar laboratoriyasi'),
    ('/labs/scratch/', 'Scratch simulyatori'),
    ('/labs/crypto/', 'Kriptografiya simulyatori'),
    ('/labs/network/', 'Tarmoqlar simulyatori'),
    ('/labs/sorting/', 'Saralash vizualizatori'),
    ('/labs/logic/', 'Mantiqiy elementlar simulyatori'),
    ('/labs/python/', 'Python terminal simulyatori'),
    ('/projects/', 'Loyihalar ustaxonasi'),
    ('/projects/assignment/1/', 'Sinf loyihasi'),
    ('/portfolio/', 'O‘quvchi portfoliosi'),
    ('/accounts/profile/', 'O‘quvchi profili va sozlamalari'),
    ('/portfolio/submission/1/', 'Topshiriq va Versiyalar tarixi'),
    ('/portfolio/submission/1/compare/', 'Dastlabki va Tuzatilgan variantlar taqqoslash'),
]

for url, name in endpoints_student:
    resp = client.get(url)
    print(f"[{resp.status_code}] {name:35} -> {url}")
    assert resp.status_code == 200, f"Xatolik: {name} ({url}) -> {resp.status_code}"

# 4. Administrator sifatida kirish
admin_user = User.objects.get(username='admin')
client.force_login(admin_user)
print("\n--- ADMINISTRATOR TESTI ---")

endpoints_admin = [
    ('/accounts/users/', 'Foydalanuvchilar boshqaruvi'),
    ('/accounts/users/add-teacher/', 'O‘qituvchi qo‘shish sahifasi'),
    ('/accounts/users/add-student/', 'O‘quvchi qo‘shish sahifasi'),
    ('/accounts/profile/', 'Admin profili'),
]

for url, name in endpoints_admin:
    resp = client.get(url)
    print(f"[{resp.status_code}] {name:35} -> {url}")
    assert resp.status_code == 200, f"Xatolik: {name} ({url}) -> {resp.status_code}"

# 5. Ruxsat cheklovi (Xavfsizlik)
print("\n--- XAVFSIZLIK VA IDOR TEKSHIRUVI ---")
client.force_login(student)
# O'quvchi dars konstruktoriga kira olmaydi
resp = client.get('/lessons/create/')
print(f"[{resp.status_code}] O‘quvchi dars konstruktoriga kirishi (kutilgan: 403) -> {resp.status_code}")
assert resp.status_code == 403

# O'quvchi o'qituvchi sinflar boshqaruviga kira olmaydi
resp = client.get('/accounts/classrooms/')
print(f"[{resp.status_code}] O‘quvchi sinflar boshqaruviga kirishi (kutilgan: 403) -> {resp.status_code}")
assert resp.status_code == 403

# O'quvchi admin foydalanuvchilar boshqaruviga kira olmaydi
resp = client.get('/accounts/users/')
print(f"[{resp.status_code}] O‘quvchi foydalanuvchilar boshqaruviga kirishi (kutilgan: 403) -> {resp.status_code}")
assert resp.status_code == 403

client.force_login(teacher)
# O'qituvchi ham admin foydalanuvchilar boshqaruviga kira olmaydi
resp = client.get('/accounts/users/')
print(f"[{resp.status_code}] O‘qituvchi foydalanuvchilar boshqaruviga kirishi (kutilgan: 403) -> {resp.status_code}")
assert resp.status_code == 403

print("\nBARCHA SAHIFALAR VA RUXSATLAR 100% MUVAFFAQIYATLI ISHLAMOQDA!")
