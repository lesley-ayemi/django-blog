from django.shortcuts import render

def page_not_found(request, exception):
    return render(request, 'errors/404.html')

def page_server_error(request):
    return render(request, 'errors/500.html')