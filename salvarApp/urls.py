from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_Accueil, name='accueil_url'),
    # province_url
    path('province', views.show_province, name='province_url' ),
    path('ajouter_province', views.ajouter_province, name='ajouter_province'),
    path('delete_province/<int:id_province>', views.delete_province, name='delete_province'),
    path('edit_province/<int:id_province>', views.editer_province, name='editer_province'),
    path('update_province/<int:id_province>', views.update_province, name='update_province'),
    path('chercher_province', views.chercher_province, name='chercher_province'),

    #commune_url
    path('commune', views.show_commune_and_charge_select, name='commune_url' ),
    path('ajouter_commune', views.ajouter_commune, name='ajouter_commune_url'),
    path('chercher_commune',views.chercher_commune_province, name='chercher_commune_url'),
    path('delete_commune/<int:id_commune>',views.delete_commune, name='delete_commune'),
    path('edit_commune/<int:id_commune>', views.edit_commune, name='edit_commune_url'),
    path('update_commune/<int:id_commune>', views.update_commune, name='update_commune_url'),

    #zone_url
    path('zone', views.show_zone, name='zone_url' ),

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
    
]
