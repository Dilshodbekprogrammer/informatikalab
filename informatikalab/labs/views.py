import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from .models import LabExperimentSubmission


def _server_verify_algorithm(algorithm_type, input_data, submitted_result):
    """Serverda algoritmni qayta hisoblaydi va yuborilgan natijani tekshiradi."""
    try:
        if algorithm_type == 'max_two':
            a = int(input_data.get('paramA', input_data.get('a', 0)))
            b = int(input_data.get('paramB', input_data.get('b', 0)))
            expected = f"Eng katta son: {max(a, b)}" if a != b else f"Sonlar teng: {a}"
        elif algorithm_type == 'even_odd':
            n = int(input_data.get('paramNumber', input_data.get('n', 0)))
            expected = f"{n} - {'juft' if n % 2 == 0 else 'toq'} son"
        elif algorithm_type == 'sum_n':
            n = int(input_data.get('paramN', input_data.get('n', 0)))
            if n < 0:
                return False, "N manfiy bo'lmasligi kerak"
            if n > 10000:
                return False, "N 10000 dan katta bo'lmasligi kerak"
            expected = f"1 dan {n} gacha yig'indi: {n*(n+1)//2}"
        else:
            return True, ""  # Noma'lum algoritmni o'tkazib yubor

        if str(submitted_result).strip() != expected.strip():
            return False, f"Noto'g'ri natija. Kutilgan: '{expected}', Yuborilgan: '{submitted_result}'"
        return True, ""
    except (ValueError, TypeError) as e:
        return False, f"Kiritilgan qiymatlar noto'g'ri: {str(e)}"


@login_required
def labs_index_view(request):
    user = request.user
    my_submissions = LabExperimentSubmission.objects.filter(student=user).order_by('-created_at')[:10]
    return render(request, 'labs/index.html', {
        'my_submissions': my_submissions
    })


@login_required
def algorithms_lab_view(request):
    user = request.user
    return render(request, 'labs/algorithms.html', {
        'user': user
    })


@login_required
def data_lab_view(request):
    user = request.user
    # Boshlang'ich 5 kunlik namunaviy ma'lumotlar (Namuna ekanligi ko'rsatiladi)
    default_data = [
        {"id": 1, "day": "Dushanba", "device": "Sinf kompyuterlari", "power": 150, "count": 12, "hours": 5.0},
        {"id": 2, "day": "Seshanba", "device": "LED yoritish tizimi", "power": 100, "count": 8, "hours": 6.0},
        {"id": 3, "day": "Chorshanba", "device": "Interaktiv proyektor", "power": 250, "count": 1, "hours": 4.0},
        {"id": 4, "day": "Payshanba", "device": "Sovutish konditsioneri", "power": 1200, "count": 1, "hours": 3.0},
        {"id": 5, "day": "Juma", "device": "Nazorat namunasi (Nazorat misoli)", "power": 100, "count": 2, "hours": 5.0},
    ]
    return render(request, 'labs/data_lab.html', {
        'default_data_json': json.dumps(default_data)
    })


@login_required
def scratch_lab_view(request):
    user = request.user
    return render(request, 'labs/scratch.html', {
        'user': user
    })


@login_required
def crypto_lab_view(request):
    user = request.user
    return render(request, 'labs/crypto.html', {
        'user': user
    })


@login_required
def network_lab_view(request):
    user = request.user
    return render(request, 'labs/network.html', {
        'user': user
    })


@login_required
def sorting_lab_view(request):
    user = request.user
    return render(request, 'labs/sorting.html', {
        'user': user
    })


@login_required
def logic_lab_view(request):
    user = request.user
    return render(request, 'labs/logic.html', {
        'user': user
    })


@login_required
def python_lab_view(request):
    user = request.user
    return render(request, 'labs/python.html', {
        'user': user
    })


@login_required
def save_experiment_api(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Faqat POST so‘rovi qabul qilinadi.")

    try:
        data = json.loads(request.body.decode('utf-8'))
        lab_type = data.get('lab_type')
        algorithm_type = data.get('algorithm_type', '')
        title = data.get('title', 'Interaktiv laboratoriya tajribasi')
        input_data = data.get('input_data', {})
        prediction = data.get('prediction', '')
        calculated_result = data.get('calculated_result', '')
        student_explanation = data.get('student_explanation', '').strip()
        additional_data = data.get('additional_data', {})

        if not student_explanation:
            return JsonResponse({'status': 'error', 'message': "Iltimos, tajriba xulosasini ('Nima o‘zgardi va nima sababdan?') to‘ldiring!"}, status=400)

        # Algoritm laboratoriyasi uchun serverda natijani tekshir
        if lab_type == 'algorithm' and algorithm_type:
            is_valid, error_msg = _server_verify_algorithm(algorithm_type, input_data, calculated_result)
            if not is_valid:
                return JsonResponse({
                    'status': 'error',
                    'message': f"Noto'g'ri natija saqlash mumkin emas. {error_msg}. Tajribani qaytadan bajaring."
                }, status=400)

        # Ma'lumotlar laboratoriyasi uchun tekshirish
        if lab_type == 'data':
            rows = additional_data.get('rows', [])
            submitted_total = additional_data.get('total_kwh', 0)
            if rows:
                try:
                    calculated_total = sum(
                        row.get('power', 0) * row.get('count', 0) * row.get('hours', 0) / 1000
                        for row in rows
                    )
                    if abs(float(submitted_total) - calculated_total) > 0.01:
                        return JsonResponse({
                            'status': 'error',
                            'message': f"Hisoblangan qiymat ({calculated_total:.2f} kWh) yuborilgan ({submitted_total:.2f} kWh) bilan mos emas."
                        }, status=400)
                except (TypeError, ValueError):
                    pass  # Ma'lumotlar to'liq bo'lmasa o'tkazib yubor

        submission = LabExperimentSubmission.objects.create(
            student=request.user,
            lab_type=lab_type,
            algorithm_type=algorithm_type if algorithm_type else None,
            title=title,
            input_data=input_data,
            prediction=prediction,
            calculated_result=str(calculated_result),
            student_explanation=student_explanation,
            additional_data=additional_data
        )

        return JsonResponse({
            'status': 'success',
            'submission_id': submission.id,
            'message': "Tajriba natijasi va tushuntirishingiz muvaffaqiyatli saqlandi!"
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
