from django.shortcuts import render,redirect
import json
from django.http import request, JsonResponse
from django.db.utils import IntegrityError
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Province, Allergie, Maladie_chronique, Centre_sanitaire, Commune, Zone, Patient, Patient_allergie, Patient_chronique, Agent_sanitaire, Agent_centre, Consultation

# Create your views here.
def show_Accueil(request):
    return render(request,"accueil.html")
# authentification view
def show_authentification(request):
    return render(request, "authentification.html")

def connexion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            try:
                profil = Agent_centre.objects.values(
                    'agent_sanitaire__profil').get(agent_sanitaire__user__username=user)
            except ObjectDoesNotExist:
                messages.info(request, "Impossible de se connecter, tu appartiens  à aucun centre sanitaire !")
                return redirect("auth_url")
            if profil['agent_sanitaire__profil'] == "administrateur":
                login(request, user)
                return redirect("agent_sanitaire_url")
            else:
                login(request, user)
                return redirect("consultation_url")
        else:
            messages.info(request, "Echec de connexion, le username ou le mot de passe est incorrecte ou tu es desactivé !")
            return redirect("auth_url")

#agent_sanitaire  ou utilisateur views
def show_agent_sanitaire(request):
    liste = Agent_sanitaire.objects.all().values('id', 'nom', 
    'prenom', 'user__username', 'user__password', 'user__is_active', 'profil')
    return render(request, "agent_sanitaire.html", locals())

def ajouter_agent_sanitaire(request):
    if request.method == 'POST':
        agent_nom = request.POST.get('nom')
        agent_prenom = request.POST.get('prenom')
        agent_username = request.POST.get('username')
        agent_password = request.POST.get('password')
        agent_etat = request.POST.get('etat')
        agent_profil = request.POST.get('profil')
        if len(agent_nom) == 0 or len(agent_prenom) == 0 or len(agent_username) == 0 or len(agent_password) == 0 or len(agent_etat) == 0 or len(agent_profil) == 0:
            messages.info(request, "Completez tous les informations svp !")
            return redirect("agent_sanitaire_url")
        else:
            try:
                user = User.objects.create_user(username=agent_username, password=agent_password, is_active=agent_etat)
            except IntegrityError :
                messages.info(request, "Echec!! le username ou le mot de passe existe déjà !")
                return redirect("agent_sanitaire_url")
            agent = Agent_sanitaire(user = user, nom = agent_nom, prenom = agent_prenom, profil = agent_profil)
            agent.save()
            messages.info(request, "La creation d'un agent sanitaire ou utilisateur reussi avec succes !")
            return redirect('agent_sanitaire_url')

def delete_agent_sanitaire(request, id_agent):
    if request.method == 'POST':
        agent = Agent_sanitaire.objects.all().get(pk=id_agent)
        users = agent.user
        agent.delete()
        users.delete()
        messages.info(request, "La suppression est reussie avec succes !")
        return redirect("agent_sanitaire_url")

def edit_agent_sanitaire(request, id_agent):
    agent = Agent_sanitaire.objects.values('id', 'nom', 'prenom', 'user__username', 'user__is_active', 'profil').get(pk=id_agent)
    return render(request, "edit_agent_sanitaire.html", {'agent':agent})

def chercher_agent_sanitaire(request):
    if request.method == 'GET':
        nom_chercher = request.GET.get('nom_chercher')
        if len(nom_chercher) == 0:
            messages.info(request, "Saisissez le nom à chercher svp !")
            return redirect("agent_sanitaire_url")
        else:
            liste = Agent_sanitaire.objects.all().values('id', 'nom', 
            'prenom', 'user__username', 'user__password', 'user__is_active', 'profil').filter(prenom=nom_chercher)
            nbr = liste.count()
            if nbr == 0:
                messages.info(request, "Cet agent sanitaire n'existe pas dans le système ou verifier l'orthographe !")
                return redirect("agent_sanitaire_url")
            else:
                return render(request, "agent_sanitaire.html", locals())

def update_agent_sanitaire(request, id_agent):
    if request.method == 'POST':
        agent = Agent_sanitaire.objects.get(pk=id_agent)
        agent.nom = request.POST.get('nom')
        agent.prenom = request.POST.get('prenom')
        agent.profil = request.POST.get('profil')
        u = agent.user
        u.is_active = request.POST.get('etat')
        u.username = request.POST.get('username')
        agent.save()
        u.save()
        messages.info(request, "La modification est reussie avec succes !")
        return redirect("agent_sanitaire_url")

#patient views
def show_patient_charge_zone(request):
    zone = Zone.objects.all()
    liste = Patient.objects.values('id', 'nom_pat', 'prenom_pat', 'groupe_sanguin', 
    'contact', 'zone__nom_zone', 'code')
    return render(request, "patient.html", locals())

def ajouter_patient(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        p_contact = request.POST.get('contact')
        p_code = request.POST.get('code')
        p_zone = request.POST.get('zone')
        g_sanguin = request.POST.get('sanguin')
        if len(nom) == 0 or len(prenom) == 0 or len(p_code) == 0 or len(p_zone) == 0 or len(g_sanguin) == 0:
            messages.info(request, "Completez toutes les informations svp !")
            return redirect('patient_url')
        else:
            p = Patient(nom_pat = nom, prenom_pat = prenom, contact = p_contact, code = p_code, zone = Zone(p_zone), groupe_sanguin = g_sanguin)
            p.save()
            messages.info(request, "Enregistrement reussi avec succes !")
            return redirect('patient_url')

def delete_patient(request, id_patient):
    if request.method == 'POST':
        Patient.objects.get(pk=id_patient).delete()
        messages.info(request, "La suppression est reussie avec succes !")
        return redirect('patient_url')

def chercher_par_code(request):
    if request.method == 'GET':
        code_chercher = request.GET.get('code_chercher')
        if len(code_chercher) == 0:
            messages.info(request, "Saisissez le code à chercher svp !")
            return redirect('patient_url')
        else:
            liste = Patient.objects.all().values('id', 
            'nom_pat', 'prenom_pat', 'groupe_sanguin', 
            'contact', 'zone__nom_zone', 'code').filter(code = code_chercher)
            nbr = liste.count()
            if nbr == 0:
                messages.info(request, "Aucun patient trouvé qui a ce code !")
                return redirect('patient_url')
            else:
                return render(request, "patient.html", locals())

def chercher_par_sanguin(request):
    if request.method == 'GET':
        groupe_chercher = request.GET.get('chercher_g')
        if len(groupe_chercher) == 0:
            messages.info(request, "Selectionnez le groupe sanguin à chercher svp !")
            return redirect('patient_url')
        else:
            liste = Patient.objects.all().values('id', 'nom_pat', 
            'prenom_pat', 'groupe_sanguin', 'contact', 'zone__nom_zone',
             'code').filter(groupe_sanguin  = groupe_chercher)
            nbr_patient = liste.count()
            if nbr_patient == 0:
                messages.info(request, "Aucun patient trouvé qui a ce groupe sanguin !")
                return redirect('patient_url')
            else:
                return render(request, "patient.html", locals())

def edit_patient(request, id_patient):
    p = Patient.objects.get(pk=id_patient)
    return render(request, "edit_patient.html", {'patient':p})

def update_patient(request, id_patient):
    if request.method == 'POST':
        p = Patient.objects.get(pk=id_patient)
        p.nom_pat = request.POST.get('nom')
        p.prenom_pat = request.POST.get('prenom')
        p.contact = request.POST.get('contact')
        p.code = request.POST.get('code')
        p.groupe_sanguin = request.POST.get('sanguin')
        p.save()
        messages.info(request, "La modification est reussie avec succes !")
        return redirect('patient_url')

#consultation view
def show_consultation(request):
    patient = Patient.objects.all()
    print(".....",request.user.id)
    agent = Agent_centre.objects.values('id', 'agent_sanitaire__nom', 
    'agent_sanitaire__prenom').get(agent_sanitaire__user__id=request.user.id)
    liste = Consultation.objects.values('id', 'patient__nom_pat', 
    'patient__prenom_pat', 'patient__code', 'agent_centre__agent_sanitaire__nom', 
    'agent_centre__agent_sanitaire__prenom', 'agent_centre__centre_sanitaire__nom_centre', 'date', 'traitement')
    return render(request, "consultation.html",locals())

def ajouter_consultation(request):
    if request.method == 'POST':
        agent = request.POST.get("agent")
        patient = request.POST.get("patient")
        traitement = request.POST.get("traitement")
        dat = request.POST.get("dates")
        if len(patient) == 0 or len(traitement) == 0:
            messages.info(request, "Completez tous les informations svp !")
            return redirect("consultation_url")
        else:
            consultation = Consultation(patient=Patient(patient), agent_centre=Agent_centre(agent), traitement=traitement, date=dat)
            consultation.save()
            messages.info(request, "Enregistrement reussi avec succes")
            return redirect("consultation_url")

def delete_consultation(request, id_consultation):
    if request.method == 'POST':
        consultation_obj = Consultation.objects.get(pk=id_consultation)
        consultation_obj.delete()
        messages.info(request, "La suppression est reussie avec succes!")
        return redirect("consultation_url")

def edit_consultation(request, id_consultation):
    consultation = Consultation.objects.get(id=id_consultation)
    print(".......",consultation.traitement)
    return render(request, "edit_consultation.html", {'consultation':consultation})

def update_consultation(request, id_consultation):
    if request.method == 'POST':
        consultation_obj = Consultation.objects.get(pk=id_consultation)
        consultation_obj.traitement = request.POST.get("traitement")
        consultation_obj.save()
        messages.info(request, "La modification est reussie avec succes !")
        return redirect("consultation_url")

def chercher_consultation_par_patient(request):
    if request.method == 'GET':
        code_chercher = request.GET.get("code_chercher")
        if  len(code_chercher) == 0:
            messages.info(request, "Saisissez d'abord le code du patient à chercher")
            return redirect("consultation_url")
        else:
            liste = Consultation.objects.values('id', 'patient__nom_pat', 
            'patient__prenom_pat', 'patient__code', 'agent_centre__agent_sanitaire__nom', 
            'agent_centre__agent_sanitaire__prenom', 'agent_centre__centre_sanitaire__nom_centre',
            'date', 'traitement').filter(patient__code=code_chercher)
            nbr = liste.count()
            if nbr == 0:
                messages.info(request, "Cet patient n'a fait aucun consultation !")
                return redirect("consultation_url")
            else:
                return render(request, "consultation.html", locals())

#patient_allergie views
def show_patient_allergie(request):
    patient = Patient.objects.all()
    allergie = Allergie.objects.all()
    liste = Patient_allergie.objects.all().values('id',
     'patient__nom_pat', 'patient__prenom_pat', 'patient__contact', 'patient__zone__nom_zone', 
     'patient__code', 'patient__groupe_sanguin', 'allergie__cause')
    return render(request, "patient_allergie.html", locals())

def ajouter_patient_allergie(request):
    if request.method == 'POST':
        p = request.POST.get('select_pat')
        a = request.POST.get('select_all')
        if len(p) == 0 or len(a) == 0:
            messages.info(request, "Selectionnez le patient et l'allergie svp !")
            return redirect('patient_allergie_url')
        else:
            try:
                pat_all = Patient_allergie(patient = Patient(p), allergie = Allergie(a))
                pat_all.save()
            except AttributeError:
                pass
            messages.info(request, "Enregistrement reussi avec succes !")
            return redirect('patient_allergie_url')

def delete_patient_allergie(request, id_pat_all):
    if request.method == 'POST':
        pat_all = Patient_allergie.objects.get(pk=id_pat_all)
        pat_all.delete()
        messages.info(request, "La suppresion est reussie avec succes")
        return redirect('patient_allergie_url')

def chercher_par_allergie(request):
    if request.method == 'GET':
        all_cherch = request.GET.get('nom_chercher')
        if len(all_cherch) == 0:
            messages.info(request, "Saisissez le nom de l'allergie à chercher svp !")
            return redirect('patient_allergie_url')
        else:
            liste = Patient_allergie.objects.all().values('id',
            'patient__nom_pat', 'patient__prenom_pat', 'patient__contact', 'patient__zone__nom_zone', 
            'patient__code', 'patient__groupe_sanguin', 'allergie__cause').filter(allergie__cause = all_cherch)
            nbr = liste.count()
            if nbr == 0:
                messages.info(request, "Pas du patient qui a cette allergie ou verifier l'orthographe !")
                return redirect('patient_allergie_url')
            else:
                return render(request, "patient_allergie.html",locals())

def chercher_par_code_patient(request):
    if request.method == 'GET':
        pat_cherch = request.GET.get('cod_chercher')
        if len(pat_cherch) == 0:
            messages.info(request, "Saisissez le code du patient à chercher")
            return redirect('patient_allergie_url')
        else:
            print(pat_cherch)
            liste = Patient_allergie.objects.all().values('id',
            'patient__nom_pat', 'patient__prenom_pat', 'patient__contact', 'patient__zone__nom_zone', 
            'patient__code', 'patient__groupe_sanguin', 'allergie__cause').filter(patient__code = pat_cherch)
            nbr = liste.count()
            if nbr == 0:
                messages.info(request, "Cet patient n'a pas d'allergie ou verifier l'orthographe !")
                return redirect('patient_allergie_url')
            else:
                return render(request, "patient_allergie.html",locals())


# province view
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

#patient_maladie_chronique_view
def show_patient_maladie_chronique(request):
    patient = Patient.objects.all()
    maladie = Maladie_chronique.objects.all()
    liste = Patient_chronique.objects.all().values('id',
            'patient__nom_pat', 'patient__prenom_pat', 'patient__contact', 'patient__zone__nom_zone', 
            'patient__code', 'patient__groupe_sanguin', 'maladie_chronique__nom_maladie')
    return render(request, "patient_maladie_chronique.html", locals())

def ajouter_patient_maladie_chronique(request):
    if request.method == 'POST':
        p = request.POST.get('select_pat')
        m = request.POST.get('select_maladie')
        if len(p) == 0 or len(m) == 0:
            messages.info(request, "Selectionnez le patient et la maladie chronique svp !")
            return redirect('patient_maladie_chronique_url')
        else:
            pat_mal = Patient_chronique(patient = Patient(p), maladie_chronique = Maladie_chronique(m))
            pat_mal.save()
            messages.info(request, "Enregistrement reussi avec succes !")
            return redirect('patient_maladie_chronique_url')

def delete_patient_maladie_chronique(request, id_pat_mal):
    if request.method == 'POST':
        pat_mal = Patient_chronique.objects.get(pk=id_pat_mal)
        pat_mal.delete()
        messages.info(request, "La suppression est reussie avec succes !")
        return redirect('patient_maladie_chronique_url')

def chercher_patient_maladie_chronique_code(request):
    if request.method == 'GET':
        code_cherch = request.GET.get('cod_chercher')
        if len(code_cherch) == 0 or len(maladie):
            messages.info(request, "Saisissez le code du patient à chercher svp !")
            return redirect('patient_maladie_chronique_url')
        else:
            liste = Patient_chronique.objects.all().values('id',
            'patient__nom_pat', 'patient__prenom_pat', 'patient__contact', 'patient__zone__nom_zone', 
            'patient__code', 'patient__groupe_sanguin', 'maladie_chronique__nom_maladie').filter(patient__code=code_cherch)
            nbr = liste.count()
            if len(nbr) == 0:
                messages.info(request, "Ce patient n'a pas d'une maladie chronique !")
                return redirect('patient_maladie_chronique_url')
            else:
                return render(request, "patient_maladie_chronique.html", locals())

def chercher_patient_maladie_chronique(request):
    if request.method == 'GET':
        mal_cherch = request.GET.get('nom_chercher')
        if len(mal_cherch) == 0:
            messages.info(request, "Saisissez le nom de la maladie à chercher svp !")
            return redirect('patient_maladie_chronique_url')
        else:
            liste = Patient_chronique.objects.all().values('id',
            'patient__nom_pat', 'patient__prenom_pat', 'patient__contact', 'patient__zone__nom_zone', 
            'patient__code', 'patient__groupe_sanguin', 'maladie_chronique__nom_maladie').filter(maladie_chronique__nom_maladie=mal_cherch)
            nbr = liste.count()
            if nbr == 0:
                messages.info(request, "Pas du patient qui a cette maladie chronique ou verifier l'orthographe !")
                return redirect('patient_maladie_chronique_url')
            else:
                return render(request, "patient_maladie_chronique.html",locals())

#agent_centre view
def show_agent_centre(request):
    agent = Agent_sanitaire.objects.all().values('id', 'nom', 'prenom', 'user__username' ,'profil')
    centre = Centre_sanitaire.objects.all()
    liste = Agent_centre.objects.all().values('id', 'agent_sanitaire__nom', 
    'agent_sanitaire__prenom', 'agent_sanitaire__profil', 'agent_sanitaire__user__username','centre_sanitaire__nom_centre')
    return render(request, "agent_centre.html", locals())

def ajouter_agent_centre(request):
    if request.method == 'POST':
        agent = request.POST.get('select_agent')
        centre = request.POST.get('select_centre')
        if len(agent) == 0 or len(centre) == 0:
            messages.info(request, "Selectionnez l'agent et le centre svp !")
            return redirect("agent_centre_url")
        else:
            agent_centre = Agent_centre(agent_sanitaire=Agent_sanitaire(agent), centre_sanitaire=Centre_sanitaire(centre))
            agent_centre.save()
            messages.info(request, "Enregistrement reussi avec succes !")
            return redirect("agent_centre_url")

def delete_agent_centre(request, id_ag_centre):
    if request.method == 'POST':
        agent_centre = Agent_centre.objects.get(pk=id_ag_centre)
        agent_centre.delete()
        messages.info(request, "La suppression est reussie avec succes !")
        return redirect("agent_centre_url")

def chercher_agent_centre_par_centre(request):
    if request.method == 'GET':
        centre_cherch = request.GET.get('centre_chercher')
        if len(centre_cherch) == 0:
            messages.info(request, "Entrez le nom du centre à chercher svp !")
            return redirect("agent_centre_url")
        else:
            liste = Agent_centre.objects.values('id', 'agent_sanitaire__nom', 
            'agent_sanitaire__prenom', 'agent_sanitaire__profil', 
            'agent_sanitaire__user__username','centre_sanitaire__nom_centre').filter(centre_sanitaire__nom_centre=centre_cherch)
            nbr = liste.count()
            if nbr == 0:
                messages.info(request, "Ce centre ne contient aucun agent sanitaire ou verifier l'orthographe !")
                return redirect("agent_centre_url")
            else:
                return render(request, "agent_centre.html", locals())

def chercher_agent_centre_par_prenom(request):
    if request.method == 'GET':
        prenom_chercher = request.GET.get('prenom_chercher')
        if len(prenom_chercher) == 0:
            messages.info(request, "Saisissez le prenom de l'agent à chercher")
            return redirect("agent_centre_url")
        else:
            liste = Agent_centre.objects.values('id', 'agent_sanitaire__nom', 
            'agent_sanitaire__prenom', 'agent_sanitaire__profil', 
            'agent_sanitaire__user__username','centre_sanitaire__nom_centre').filter(agent_sanitaire__prenom=prenom_chercher)
            nbr = liste.count()
            if nbr == 0:
                messages.info(request, "L'agent que vous cherchez n'existe pas ou verifier l'orthographe !")
                return redirect("agent_centre_url")
            else:
                return render(request, "agent_centre.html", locals())
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

def chercher_commune(request):
    if request.method == 'GET':
        nom = request.GET.get('nom_chercher_com')
        if len(nom) == 0:
            messages.info(request, "Saisissez le nom de la commune à chercher svp !")
            return redirect('commune_url')
        else:
            liste = Commune.objects.all().values('id','province__nom_province','nom_commune').filter(nom_commune=nom)
            nbr = liste.count()
            if nbr == 0:
                messages.info(request, "La commune n'existe pas dans le system ou verifier l'orthographe svp !")
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
def show_zone_charge_select(request):
    select_commune = Commune.objects.all()
    liste =  Zone.objects.all().values('id', 'commune__nom_commune', 'nom_zone')
    return render(request, "zone.html", locals())

def ajouter_zone(request):
    if request.method == 'POST':
        nom_commune = request.POST.get('select_com')
        nom = request.POST.get('zone')
        if len(nom) == 0:
            messages.info(request, "Saisissez le nom svp !")
            return redirect('zone_url')
        elif len(nom_commune) == 0:
            messages.info(request, "Selectionnez la commune svp !")
            return redirect('zone_url')
        else:
            z = Zone(nom_zone=nom, commune=Commune(nom_commune))
            z.save()
            messages.info(request, "Enregistrement reussi avec succes !")
            return redirect('zone_url')

def delete_zone(request, id_zone):
    if request.method == 'POST':
        Zone.objects.get(id=id_zone).delete()
        messages.info(request, "La suppression est reussie avec succes !")
        return redirect('zone_url')

def edit_zone(request, id_zone):
    zone = Zone.objects.get(id=id_zone)
    return render(request, "edit_zone.html", {'zone':zone})

def update_zone(request, id_zone):
    if request.method == 'POST':
        z = Zone.objects.get(pk=id_zone)
        z.nom_zone = request.POST.get('nom')
        z.save()
        messages.info(request, "La modification est reussie !")
        return redirect('zone_url')

def chercher_zone_commune(request):
    if request.method == 'GET':
        nom = request.GET.get('nom_chercher_com')
        if len(nom) == 0:
            messages.info(request, "Saisissez le nom de la commune à chercher")
            return redirect("zone_url")
        else:
            liste = Zone.objects.all().values('id', 'commune__nom_commune', 'nom_zone').filter(commune_nom_commune=nom)
            nbr = liste.count()
            if nbr == 0:
                messages.info(request, "La zone que vous cherchez n'exitse dans le systeme ou verifiez l'orthographe !")
                return redirect('zone_url')
            else:
                return render(request, "zone.html", {'liste':liste})

def chercher_zone(request):
    if request.method == 'GET':
        nom = request.GET.get('nom_chercher')
        if len(nom) == 0:
            messages.info(request, "Saisissez le nom du zone à chercher")
            return redirect("zone_url")
        else:
            liste = Zone.objects.all().values('id', 'commune__nom_commune', 'nom_zone').filter(nom_zone=nom)
            nbr = liste.count()
            if nbr == 0:
                messages.info(request, "La commune ne contient aucune zone dans le système ou verifier l'orthographe svp !")
                return redirect('zone_url')
            else:
                return render(request, "zone.html", {'liste':liste})
    
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


