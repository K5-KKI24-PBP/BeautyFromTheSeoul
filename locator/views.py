from django.shortcuts import render

def show_locator(request):
    return render(request, 'locator.html')
