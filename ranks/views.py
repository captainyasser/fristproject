from django.shortcuts import render, redirect, get_object_or_404
from .models import Rank
from .forms import RankForm




def rank_list(request):
    ranks = Rank.objects.all().order_by('rank_type', 'order')  # ترتيب حسب نوع الدرجة ثم الترتيب
    form = RankForm()  # نموذج الإضافة
    return render(request, 'ranks/ranks.html', {'ranks': ranks, 'form': form})

def add_rank(request):
    if request.method == 'POST':
        form = RankForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rank_list')
        ranks = Rank.objects.all()
        return render(request, 'ranks/ranks.html', {'ranks': ranks, 'form': form})
    return redirect('rank_list')

def edit_rank(request, rank_id):
    rank = get_object_or_404(Rank, id=rank_id)
    if request.method == 'POST':
        form = RankForm(request.POST, instance=rank)
        if form.is_valid():
            form.save()
            return redirect('rank_list')
        ranks = Rank.objects.all()
        return render(request, 'ranks/ranks.html', {'ranks': ranks, 'form': RankForm(), 'edit_form': form})
    # عند GET، نعيد الصفحة مع نموذج التعديل
    ranks = Rank.objects.all()
    edit_form = RankForm(instance=rank)
    return render(request, 'ranks/ranks.html', {'ranks': ranks, 'form': RankForm(), 'edit_form': edit_form})

def delete_rank(request, rank_id):
    rank = get_object_or_404(Rank, id=rank_id)
    if request.method == 'POST':
        rank.delete()
    return redirect('rank_list')