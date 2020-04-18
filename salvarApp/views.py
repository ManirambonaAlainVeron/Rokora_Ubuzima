from django.shortcuts import render,redirect
import json
from django.http import request, JsonResponse
from django.contrib import messages
from .models import Province,Allergie,Maladie_chronique,Centre_sanitaire,Commune

# Create your views here.
def show_Accueil(request):
    return render(request,"accueil.html")

def show_province(request):
    liste = Province.objects.all().order_by('id')
    return render(request, "province.html", locals())

def ajouter_province(request):
    if request.method == 'POST':
        nom_prov = request.POST.get("nom_province")
        if len(nom_prov) == 0:
            messages.info(request, "Entrez le nom du province svp !")
            return redirect('province_url')
        else:
            p = Province(nom_province = nom_prov)
            p.save()
            messages.info(request, "Ajout reussi avec succes !")
            return redirect('province_url')

def delete_province(request, id_province):
    Province.objects.get(id=id_province).delete()
    messages.info(request, "La suppresion est reussie avec succes !")
    return redirect('province_url')

def editer_province(request, id_province):
    province = Province.objects.get(id=id_province)
    return render(request, "edit_province.html", {'province':province})

def update_province(request, id_province):
    if request.method == 'POST':
        p = Province.objects.get(pk=id_province)
        p.nom_province=request.POST.get("nom")
        p.save()
        messages.info(request, "La modification reussie avec succes !")
        return redirect('province_url')

def chercher_province(request):
    if request.method == 'GET':
        nom = request.GET.get('nom_chercher')
        if len(nom) == 0:
            messages.info(request, "Entrez le nom du province à chercher svp !")
            return redirect('province_url')
        else:
            liste = Province.objects.all().filter(nom_province=nom)
            nbr = Province.objects.all().filter(nom_province=nom).count()
            if nbr == 0:
                messages.info(request, "Cette province n'existe pas verifier l'orthographe svp le nom doit commencé par majuscule ! ")
                return redirect('province_url')
            else:
                return render(request, "province.html", {'liste':liste})

#commune view
def show_commune_and_charge_select(request):
    select_province = Province.objects.all()
    liste = Commune.objects.all().values('id','province__nom_province','nom_commune')
    return render(request, "commune.html",locals())

def chercher_commune_province(request):
    if request.method == 'GET':
        nom = request.GET.get('nom_chercher')
        if len(nom) == 0:
            messages.info(request, "Saisissez le nom de la province que vous chercher svp !")
            return redirect('commune_url')
        else:
            liste = Commune.objects.all().values('id','province__nom_province','nom_commune').filter(province__nom_province=nom)
            nbr = liste.count()
            if nbr == 0:
                messages.info(request, "La province ne contient aucune commune dans le system ou verifier l'orthographe svp !")
                return redirect('commune_url')
            else:
                return render(request, "commune.html",{'liste':liste})

def ajouter_commune(request):
    if request.method == 'POST':
        pro = request.POST.get('select_pro')
        com = request.POST.get('commune')
        if len(pro) == 0:
            messages.info(request, "Selectionnez le province svp !")
            return redirect('commune_url')
        elif len(com) == 0:
            messages.info(request, "Saisissez la commune svp !")
            return redirect('commune_url')
        else:
            c = Commune(province = Province(pro), nom_commune = com)
            c.save()
            messages.info(request, "Enregistrement reussi avec succes !")
            return redirect('commune_url')

def delete_commune(request, id_commune):
    if request.method == 'POST':
        Commune.objects.get(pk=id_commune).delete()
        messages.info(request, "La suppression est reussie avec succes !")
        return redirect('commune_url')

def edit_commune(request, id_commune):
    commune = Commune.objects.get(pk=id_commune)
    return render(request, "edit_commune.html", locals())

def update_commune(request, id_commune):
    if request.method == 'POST':
        c = Commune.objects.get(pk=id_commune)
        c.nom_commune = request.POST.get('nom')
        c.save()
        messages.info(request, "La modification est reussie avec succes !")
        return redirect('commune_url')

#zone views
def show_zone(request):
    return render(request, "zone.html")

#allergie views
def show_allergie(request):
    liste = Allergie.objects.all().order_by('id')
    return render(request, "allergie.html", locals())

def ajouter_allergie(request):
    if request.method == 'POST':
        allergie_cause = request.POST.get('cause')
        if len(allergie_cause) == 0:
            messages.info(request, "Donner la cause svp !")
            return redirect('allergie_url')
        else:
            a = Allergie(cause = allergie_cause)
            a.save()
            messages.info(request, "Enregistrement reussi avec succes !")
            return redirect('allergie_url')

def delete_allergie(request, id_allergie):
    if request.method == 'POST':
        Allergie.objects.get(id=id_allergie).delete()
        messages.info(request, "La suppression est reussie avec succes !")
        return redirect('allergie_url')

def edite_allergie(request, id_allergie):
    if request.method == 'POST':
        allergie = Allergie.objects.get(id = id_allergie)
        return render(request, "edit_allergie.html", {'allergie':allergie})

def update_allergie(request, id_allergie):
    if request.method == 'POST':
        a = Allergie.objects.get(pk=id_allergie)
        a.cause = request.POST.get('nom')
        a.save()
        messages.info(request, "La modification est reussie avec succes !")
        return redirect('allergie_url')

def chercher_allergie(request):
    if request.method == 'GET':
        nom_cause = request.GET.get('nom_chercher')
        if len(nom_cause) == 0:
            messages.info(request, "Entrez la cause à chercher svp !")
            return redirect('allergie_url')
        else:
            liste = Allergie.objects.all().filter(cause = nom_cause)
            nbr = liste.count()
            if(nbr == 0):
                messages.info(request, "Cette allergie n'existe pas !")
                return redirect('allergie_url')
            else:
                return render(request, "allergie.html", {'liste':liste})

#maladie chronique views
def show_maladie_chronique(request):
    liste = Maladie_chronique.objects.all()
    return render(request, "maladie_chronique.html", locals())

def ajouter_maladie_chronique(request):
    if request.method ==  'POST':
        maladie = request.POST.get('nom_mal')
        if len(maladie) == 0:
            messages.info(request, "Entrez le nom de la maladie svp !")
            return redirect('maladie_url')
        else:
            m =  Maladie_chronique(nom_maladie = maladie)
            m.save()
            messages.info(request, "Enregistrement reussi avec succes !")
            return redirect('maladie_url')

def delete_maladie_chronique(request, id_maladie):
    Maladie_chronique.objects.get(id=id_maladie).delete()
    messages.info(request, "La suppression est reussie avec succes !")
    return redirect('maladie_url')

def edit_maladie_chronique(request, id_maladie):
    if request.method == 'POST':
        maladie = Maladie_chronique.objects.get(id=id_maladie)
        return render(request, "edit_maladie_chronique.html", {'maladie':maladie})

def update_maladie(request, id_maladie):
    if request.method == 'POST':
        m = Maladie_chronique.objects.get(pk=id_maladie)
        m.nom_maladie = request.POST.get('nom_mal')
        m.save()
        messages.info(request, "La modification est reussie avec succes !")
        return redirect('maladie_url')

def chercher_maladie_chronique(request):
    if request.method == 'GET':
        maladie = request.GET.get('maladie_chercher')
        if len(maladie) == 0:
            messages.info(request, "Entrez la maladie à chercher")
            return redirect('maladie_url')
        else:
            liste = Maladie_chronique.objects.all().filter(nom_maladie=maladie)
            nbr = liste.count()
            if nbr == 0:
                messages.info(request, "La maladie cherchée n'existe pas ou verifier l'orthographe")
                return redirect('maladie_url')
            else:
                return render(request, "maladie_chronique.html", {'liste':liste})

#centre sanitaire views
def show_centre_sanitaire(request):
    liste = Centre_sanitaire.objects.all().order_by('id')
    return render(request, "centre_sanitaire.html", locals())

def ajouter_centre_sanitaire(request):
    if request.method == 'POST':
        centre = request.POST.get('nom_centre')
        if len(centre) == 0:
            messages.info(request, "Entrez le nom du centre svp !")
            return redirect('centre_url')
        else:
            c = Centre_sanitaire(nom_centre = centre)
            c.save()
            messages.info(request, "Enregistrement reussi avec succes !")
            return redirect('centre_url')

def delete_centre_sanitaire(request, id_centre):
    if request.method == 'POST':
        Centre_sanitaire.objects.get(id=id_centre).delete()
        messages.info(request, "La suppression est reussie avec succes !")
        return redirect('centre_url')

def edit_centre_sanitaire(request, id_centre):
    if request.method == 'POST':
        centre = Centre_sanitaire.objects.get(pk=id_centre)
        return render(request, "edit_centre_sanitaire.html", {'centre':centre})

def update_centre_sanitaire(request, id_centre):
    if request.method == 'POST':
        c = Centre_sanitaire.objects.get(pk=id_centre)
        c.nom_centre = request.POST.get('nom_centre')
        c.save()
        messages.info(request, "La modification est reussie avec succes !")
        return redirect('centre_url')

def chercher_centre_sanitaire(request):
    if request.method == 'GET':
        nom_chercher = request.GET.get('centre_chercher')
        if len(nom_chercher) == 0:
            messages.info(request, "Entrez le nom du centre à chercher svp !")
            return redirect('centre_url')
        else:
            centre = Centre_sanitaire.objects.all().filter(nom_centre=nom_chercher)
            nbr = centre.count()
            if nbr == 0:
                messages.info(request, "Le centre sanitaire que vous chercher n'existe pas ou verifier l'orthographe !")
                return redirect('centre_url')
            else:
                return render(request, "centre_sanitaire.html", {'liste':centre})


