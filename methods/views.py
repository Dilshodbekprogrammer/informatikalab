from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import TeachingMethod


@login_required
def methods_list_view(request):
    methods = TeachingMethod.objects.filter(is_active=True).order_by('order')
    return render(request, 'methods/list.html', {'methods': methods})


@login_required
def method_detail_view(request, slug):
    method = get_object_or_404(TeachingMethod, slug=slug, is_active=True)
    return render(request, 'methods/detail.html', {'method': method})
