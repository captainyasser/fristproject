from django.shortcuts import render, redirect, get_object_or_404
from .models import Rank
from .forms import RankForm

def rank_list(request):
    ranks = Rank.objects.all()  # جلب جميع الدرجات
    form = RankForm()
    return render(request, 'ranks/ranks.html', {'ranks': ranks, 'form': form})

def add_rank(request):
    if request.method == 'POST':
        form = RankForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rank_list')  # إعادة توجيه بعد الإضافة
    return redirect('rank_list')

def edit_rank(request, rank_id):
    rank = get_object_or_404(Rank, id=rank_id)
    if request.method == 'POST':
        form = RankForm(request.POST, instance=rank)
        if form.is_valid():
            form.save()
            return redirect('rank_list')
    return redirect('rank_list')

def delete_rank(request, rank_id):
    rank = get_object_or_404(Rank, id=rank_id)
    rank.delete()
    return redirect('rank_list')
