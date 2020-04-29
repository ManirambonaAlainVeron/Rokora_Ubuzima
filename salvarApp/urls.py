from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_authentification, name='auth_url'),
    path('connexion', views.connexion, name='connexion_url'),

    # patient_url
    path('patient', views.show_patient_charge_zone, name='patient_url'),
    path('ajouter_patient', views.ajouter_patient, name='ajouter_patient_url'),
    path('delete_patient/<int:id_patient>', views.delete_patient, name='delete_patient_url'),
    path('edit_patient/<int:id_patient>', views.edit_patient, name='edit_patient_url'),
    path('update_patient/<int:id_patient>', views.update_patient, name='update_patient_url'),
    path('chercher_code', views.chercher_par_code, name='chercher_code_url'),
    path('chercher_groupe', views.chercher_par_sanguin, name='chercher_sanguin_url'),
    path('chercher_patient_par_zone', views.chercher_patient_par_zone ,name='chercher_patient_par_zone_url'),

    # consultation_url
    path('consultation', views.show_consultation, name='consultation_url'),
    path('ajouter_consultation', views.ajouter_consultation, name='ajouter_consultation_url'),
    path('delete_consultation/<int:id_consultation>', views.delete_consultation, name='delete_consultation_url'),
    path('edit_consultation/<int:id_consultation>', views.edit_consultation, name='edit_consultation_url'),
    path('update_consultation/<int:id_consultation>', views.update_consultation, name='update_consultation_url'),
    path('chercher_consultation_patient', views.chercher_consultation_par_patient, name='chercher_consultation_url'),

    # patient_allergie_url
    path('patient_allergie', views.show_patient_allergie, name='patient_allergie_url'),
    path('ajouter_patient_allergie', views.ajouter_patient_allergie, name='ajouter_patient_allergie_url'),
    path('delete_patient_allergie/<int:id_pat_all>', views.delete_patient_allergie, name='delete_patient_allergie_url'),
    path('chercher_patient_allergie_code', views.chercher_par_code_patient, name='chercher_patient_allergie_code_url'),
    path('chercher_patient_allergie', views.chercher_par_allergie, name='chercher_patient_allergie_url'),

    # agent_sanitaire_url
    path('agent_sanitaire', views.show_agent_sanitaire, name='agent_sanitaire_url'),
    path('ajouter_agent_sanitaire', views.ajouter_agent_sanitaire, name='ajouter_agent_sanitaire_url'),
    path('delete_agent_sanitaire/<int:id_agent>', views.delete_agent_sanitaire, name='delete_agent_sanitaire_url'),
    path('edit_agent_sanitaire/<int:id_agent>', views.edit_agent_sanitaire, name='edit_agent_sanitaire_url'),
    path('update_agent_sanitaire/<int:id_agent>', views.update_agent_sanitaire, name='update_agent_sanitaire_url'),
    path('chercher_agent_sanitaire', views.chercher_agent_sanitaire, name='chercher_agent_sanitaire_url'),

    # province_url
    path('province', views.show_province, name='province_url' ),
    path('ajouter_province', views.ajouter_province, name='ajouter_province'),
    path('delete_province/<int:id_province>', views.delete_province, name='delete_province'),
    path('edit_province/<int:id_province>', views.editer_province, name='editer_province'),
    path('update_province/<int:id_province>', views.update_province, name='update_province'),
    path('chercher_province', views.chercher_province, name='chercher_province'),

    #patient_maladie_chronique_url
    path('patient_maladie_chronique', views.show_patient_maladie_chronique, name='patient_maladie_chronique_url'),
    path('ajouter_patient_maladie_chronique', views.ajouter_patient_maladie_chronique, name='ajouter_patient_maladie_chronique_url'),
    path('delete_patient_maladie_chronique/<int:id_pat_mal>', views.delete_patient_maladie_chronique, name='delete_patient_maladie_chronique_url'),
    path('chercher_patient_maladie_chronique_code', views.chercher_patient_maladie_chronique_code, name='chercher_patient_maladie_chronique_code_url'),
    path('chercher_patient_maladie_chronique', views.chercher_patient_maladie_chronique, name='chercher_patient_maladie_chronique_url'),

    #commune_url
    path('commune', views.show_commune_and_charge_select, name='commune_url' ),
    path('ajouter_commune', views.ajouter_commune, name='ajouter_commune_url'),
    path('chercher_commune_province',views.chercher_commune_province, name='chercher_commune_pro_url'),
    path('chercher_commune',views.chercher_commune, name='chercher_commune_url'),
    path('delete_commune/<int:id_commune>',views.delete_commune, name='delete_commune'),
    path('edit_commune/<int:id_commune>', views.edit_commune, name='edit_commune_url'),
    path('update_commune/<int:id_commune>', views.update_commune, name='update_commune_url'),

    #zone_url
    path('zone', views.show_zone_charge_select, name='zone_url' ),
    path('ajouter_zone', views.ajouter_zone, name='ajouter_zone_url'),
    path('chercher_zone',views.chercher_zone, name='chercher_zone_url'),
    path('chercher_zone_commune',views.chercher_zone_commune, name='chercher_zone_com_url'),
    path('delete_zone/<int:id_zone>',views.delete_zone, name='delete_zone_url'),
    path('edit_zone/<int:id_zone>', views.edit_zone, name='edit_zone_url'),
    path('update_zone/<int:id_zone>', views.update_zone, name='update_zone_url'),

    # allergie_url
    path('allergie', views.show_allergie, name='allergie_url' ),
    path('ajouter_allergie', views.ajouter_allergie, name='ajouter_allergie'),
    path('delete_allergie/<int:id_allergie>', views.delete_allergie, name='delete_allergie'),
    path('edit_allergie/<int:id_allergie>', views.edite_allergie, name='edit_allergie'),
    path('update_allergie/<int:id_allergie>', views.update_allergie, name='update_allergie'),
    path('chercher_allergie', views.chercher_allergie, name='chercher_allergie'),

    #centre_sanitaire_url
    path('centre_sanitaire', views.show_centre_sanitaire, name='centre_url' ),
    path('ajouter_centre_sanitaire', views.ajouter_centre_sanitaire, name='ajouter_centre_url'),
    path('delete_centre_sanitaire/<int:id_centre>', views.delete_centre_sanitaire, name='delete_centre_url'),
    path('edit_centre_sanitaire/<int:id_centre>', views.edit_centre_sanitaire, name='edit_centre_url'),
    path('update_centre_sanitaire/<int:id_centre>', views.update_centre_sanitaire, name='update_centre_url'),
    path('chercher_centre_sanitaire', views.chercher_centre_sanitaire, name='chercher_centre_url'),

    #maladie chronique
    path('maladie_chronique', views.show_maladie_chronique, name='maladie_url' ),
    path('ajouter_maladie_chronique', views.ajouter_maladie_chronique, name='ajouter_maladie_url'),
    path('delete_maladie_chronique/<int:id_maladie>', views.delete_maladie_chronique, name='delete_maladie_url'),
    path('edit_maladie_chronique/<int:id_maladie>', views.edit_maladie_chronique, name='edit_maladie_url'),
    path('update_maladie_chronique/<int:id_maladie>', views.update_maladie, name='update_maladie_url'),
    path('chercher_maladie_chrpnique', views.chercher_maladie_chronique, name='chercher_maladie_url'),

    #agent_centre
    path('agent_centre', views.show_agent_centre, name='agent_centre_url'),
    path('ajouter_agent_centre', views.ajouter_agent_centre, name='ajouter_agent_centre_url'),
    path('delete_agent_centre/<int:id_ag_centre>', views.delete_agent_centre, name='delete_agent_centre_url'),
    path('chercher_agent_centre_par_centre', views.chercher_agent_centre_par_centre, name='chercher_agent_centre_par_centre_url'),
    path('chercher_agent_centre_par_prenom', views.chercher_agent_centre_par_prenom, name='chercher_agent_centre_par_prenom_url'),
    
]
