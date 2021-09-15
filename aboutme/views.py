from aboutme.forms import BioForm
from django.shortcuts import redirect, render
from .models import Biography
# Create your views here.
# def aboutMe(request):
#     about = Biography.objects.all()
#     context = {
#         'about':about
#     }
#     return render(request,'blog/main.html', context)

# def Biography(request):
#     form = BioForm()
#     return render(request, 'dashboard/profile/bio.html', {'form':form})