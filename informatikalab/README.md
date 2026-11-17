# InformatikaLab — Zamonaviy Yondashuvlar va Xorijiy Tajribalar Integratsiyasi Platformasi

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1%2B-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-100%25%20Ishchi%20Holatda-brightgreen.svg)]()
[![Offline](https://img.shields.io/badge/Offline-100%25%20Mahalliy%20Kutubxonalar-orange.svg)]()

> **Mavzu:** Zamonaviy yondashuvlar va xorijiy tajribalar integratsiyasi yordamida informatika fanini o‘qitish.  
> **Maqsadli auditoriya:** 9-sinf informatika fani o‘qituvchi va o‘quvchilari.  
> **Asosiy ta'lim zanjiri:**  
> `1. Metod tanlash` → `2. Darsni loyihalash` → `3. Interaktiv laboratoriya` → `4. Mahsulot yaratish (loyiha)` → `5. O‘qituvchi izohi` → `6. Takomillashtirish`.

---

## 📌 Loyiha Haqida

**InformatikaLab** — umumiy o‘rta ta’lim maktablarining 9-sinf o‘quvchilariga informatika va axborot texnologiyalari fanini xorijiy ta'lim andozalari (Estoniya, Finlandiya, Buyuk Britaniya) asosida, passiv eshituvchilikdan faol tadqiqotchilikka o‘tkazgan holda o‘qitish uchun mo‘ljallangan milliy ta’limiy web-platforma.

Platforma **100% oflayn** ishlashga moslashtirilgan bo‘lib, maktablarda internet tezligi cheklangan yoki yo‘q sharoitda ham hech qanday tashqi CDN yoki bulut xizmatlariga ulanmasdan to‘liq ishlaydi.

---

## 🔬 8 ta Interaktiv Laboratoriya Simulyatori

| № | Laboratoriya | Xorijiy metod va mavzu | Asosiy imkoniyatlari |
|---|---|---|---|
| 1 | **Algoritmlar** | Tarmoqlanuvchi va takrorlanuvchi algoritmlar | 3 ta algoritm (kattasini topish, juft/toq, $1..N$ yig‘indisi), psevdokod, jonli o‘zgaruvchilar jadvali (Live Watch Table), gipoteza tekshiruvi. |
| 2 | **Ma’lumotlar tahlili** | PBL: Maktab elektr energiyasini tejash | Dinamik hisob-kitob jadvali, Chart.js interaktiv grafiklari (chiziqli va ustunli), tejash ssenariysini modellashtirish. |
| 3 | **Scratch dasturlash** | Buyuk Britaniya: Blokli dasturlash va geometriya | Oltiburchak, sakkizburchak, yulduz kabi shakllarni erkin chizish, bloklarni siljitish, parametrlarni o‘zgartirish, Web Audio tovush effektlari. |
| 4 | **Kriptografiya** | Kiberxavfsizlik va axborot himoyasi | Sezar shifri (ROT 1–25), ikkilik ASCII XOR shifrlagich, parollar mustahkamligi va entropiya (bit) hisoblagichi. |
| 5 | **Kompyuter tarmoqlari** | Tarmoq arxitekturasi va marshrutlash | Yulduz (Star), Shina (Bus), Halqa (Ring) topologiyalari, jonli ping paketi animatsiyasi, kabel uzilish avariyasi testi, IPv4 CIDR subnetting. |
| 6 | **Saralash va qidiruv** | Algoritmik samaradorlik | Pufaksimon (Bubble sort), Tanlash (Selection sort) va Ikkilik qidiruv (Binary search) animatsiyalari, taqqoslash va almashtirishlar hisoblagichlari. |
| 7 | **Mantiqiy sxemalar** | Raqamli sxemotexnika va kompyuter tuzilishi | AND, OR, NOT, XOR, NAND ventillari, jonli o‘chirgichlar (0/1), dinamik rostlik jadvallari, 1-bitli Half-Adder (jamlagich) mikrosxemasi. |
| 8 | **Python terminali** | Matnli dasturlash (Python 3) | Brauzer ichidagi sof oflayn Python interpretatori, `input()`, `int()`, `float()`, `for`/`while`, shartlar, ro‘yxatlar, cheksiz sikllardan himoya. |

---

## 📚 7 ta Namunaviy Sinf Loyihasi (4 Darslik Tizim)

Har bir loyiha 4 bosqichli amaliy darsga ajratilgan va tegishli laboratoriya bilan bog‘langan:

1. **Maktabda elektr energiyasidan oqilona foydalanish** — *Ma’lumotlar laboratoriyasi (`/labs/data/`)*
2. **Smart School: Scratch orqali ta’limiy o‘yin yaratish** — *Scratch laboratoriyasi (`/labs/scratch/`)*
3. **Maktab axborot tizimini kiberhujumlardan himoyalash** — *Kriptografiya laboratoriyasi (`/labs/crypto/`)*
4. **Kompyuter sinfi lokal tarmog‘ini loyihalash** — *Kompyuter tarmoqlari (`/labs/network/`)*
5. **Kutubxona kitoblarini saralash va tezkor qidirish** — *Saralash laboratoriyasi (`/labs/sorting/`)*
6. **Ikkilik kalkulyator va mantiqiy sxemalar modeli** — *Mantiqiy sxemalar (`/labs/logic/`)*
7. **Python tilida avtomatlashtirilgan baholash dasturi** — *Python laboratoriyasi (`/labs/python/`)*

---

## 🌍 5 ta Xalqaro Pedagogik Metod

- **Loyiha asosida o‘qitish (Project-Based Learning — PBL)** — Estoniya *ProgeTiigri* dasturi;
- **Muammoli ta’lim (Problem-Based Learning)** — Finlandiya *EDUFI OPS 2016* fenomeni;
- **Juftlikda dasturlash (Pair Programming)** — Buyuk Britaniya *NCCE* 12 pedagogika tamoyili (Driver & Navigator rollari);
- **Tadqiqot va tajriba orqali o‘rganish (Inquiry-Based Learning)** — Buyuk Britaniya *DfE Computing* standarti;
- **Teskari sinf (Flipped Classroom)** — Estoniya raqamli maktab amaliyoti (*e-School / Opiq*).

---

## 👥 Foydalanuvchilar va Sinflar Boshqaruvi

- **Administrator:**
  - O‘qituvchilar va o‘quvchilar hisoblarini qo‘shish, tahrirlash va parollarini yangilash;
  - Sinflar (9-A, 9-B va h.k.) yaratish va mas'ul o‘qituvchini biriktirish;
  - Foydalanuvchilarni o‘chirish yoki faolligini nazorat qilish.
- **O‘qituvchi:**
  - O‘z profili, logini (foydalanuvchi nomi) va parolini mustaqil tahrirlash;
  - O‘z sinfiga yangi o‘quvchi hisobini joyida yaratish va biriktirish;
  - Dars konstruktori orqali dars loyihalash (vaqt balansi tekshiruvi bilan);
  - O‘quvchilar topshirgan loyihalarni tekshirish, izoh (feedback) berish va qayta ishlashga yuborish.
- **O‘quvchi:**
  - Biriktirilgan darslarni ko‘rish va laboratoriyalarda tajriba o‘tkazish;
  - Topshiriqlar versiyalarini (v1, v2...) yuklash va taqqoslash (Diff);
  - Refleksiya yozish va portfolioga saqlash.

---

## 🚀 O‘rnatish va Ishga Tushirish

### 1. Repozitoriyni klonlash
```bash
git clone https://github.com/username/informatikalab.git
cd informatikalab
```

### 2. Virtual muhitni faollashtirish
```bash
# macOS / Linux:
python3 -m venv venv
source venv/bin/activate

# Windows:
python -m venv venv
venv\Scripts\activate
```

### 3. Bog‘liqliklarni o‘rnatish
```bash
pip install -r requirements.txt
```

### 4. Ma’lumotlar bazasini tayyorlash
```bash
cd informatikalab
python manage.py migrate
```

### 5. Namunaviy ma’lumotlarni yuklash (Seed Data)
Barcha 8 ta laboratoriya, 7 ta loyiha, 5 ta metod va namunaviy foydalanuvchilar avtomatik yaratiladi:
```bash
python manage.py seed_data
```

### 6. Serverni ishga tushirish
```bash
python manage.py runserver 127.0.0.1:8000
```
Brauzerda oching: **`http://127.0.0.1:8000/`**

---

## 🔑 Test Hisoblari (Login va Parollar)

| Rol | F.I.SH | Login | Parol | Mas'uliyati |
| :--- | :--- | :--- | :--- | :--- |
| **Administrator** | Tizim Administratori | `admin` | `admin123` | Barcha o‘qituvchilar, o‘quvchilar va sinflarni boshqarish |
| **O‘qituvchi** | Jasur Karimov | `oqituvchi` | `oqituvchi123` | 9-A sinf o‘qituvchisi, dars loyihalash, portfolio tekshiruvi |
| **O‘qituvchi (2)** | Malika Akbarova | `malika_oqituvchi` | `oqituvchi123` | 9-B sinf o‘qituvchisi, robototexnika va STEAM loyihalari |
| **O‘quvchi** | Anvar Saidov | `oquvchi1` | `oquvchi123` | 9-A sinf o‘quvchisi, guruh yetakchisi, laboratoriya tadqiqotchisi |
| **O‘quvchi** | Madina Alimova | `oquvchi2` | `oquvchi123` | 9-A sinf o‘quvchisi, tahlil va grafiklar bilan ishlovchi a'zo |
| **O‘quvchi** | Nodirbek Zokirov | `nodir` | `oquvchi123` | 9-A sinf o‘quvchisi |
| **O‘quvchi** | Dilnoza Rahimova | `dilnoza` | `oquvchi123` | 9-B sinf o‘quvchisi |

---

## 🧪 Avtomatlashtirilgan Testlar

Tizim ishonchliligini tekshirish uchun barcha unit va smoke testlarni ishga tushirish mumkin:

```bash
# 20 ta Django unit testlari:
python manage.py test

# 51 ta sahifa va xavfsizlik (IDOR) smoke testi:
python smoke_test.py
```

---

## 📄 Litsenziya

Loyiha [MIT Litsenziyasi](LICENSE) asosida erkin tarqatiladi. Ta’lim muassasalarida bepul foydalanish va moslashtirish uchun ochiq.
