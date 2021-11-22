from marketing.forms import SubscribeForm
from django.shortcuts import render
from django.views.generic import View, FormView, CreateView

# Create your views here.
# def newsletter(request):
#     form = SubscribeForm()
#     return render(request, 'blog/main.html', {'form':form})
class HomeView(CreateView):
    template_name = 'partials/home-sidebar.html'
    form_class = SubscribeForm
    success_url = '/'

    # def form_v
    