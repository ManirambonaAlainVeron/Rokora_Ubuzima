from django.shortcuts import render

# Create your views here.
def show_Accueil(request):
    return render(request,"accueil.html")

