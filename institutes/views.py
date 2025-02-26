from django.shortcuts import render, redirect
from institutes.forms import InstituteForm

def add_institute(request):
    if request.method == "POST":
        form = InstituteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  
    else:
        form = InstituteForm()
    return render(request, 'institutes/add_institute.html', {'form': form})
