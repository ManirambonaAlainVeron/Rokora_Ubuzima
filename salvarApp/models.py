from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Agent_sanitaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    profil = models.CharField(max_length=50)

    class Meta:
        db_table = 'Agent_sanitaire'

    
class Province(models.Model):
    nom_province = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'Province'


class Commune(models.Model):
    nom_commune = models.CharField(max_length=50)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    class Meta:
        db_table = 'commune'


class Zone(models.Model):
    nom_zone = models.CharField(max_length=50)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Zone'

class Patient(models.Model):
    nom_pat = models.CharField(max_length=50)
    prenom_pat = models.CharField(max_length=50)
    contact = models.IntegerField()
    code = models.CharField(max_length=100)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    groupe_sanguin = models.CharField(max_length=3)

    class Meta:
        db_table = 'Patient'


class Maladie_chronique(models.Model):
    nom_maladie = models.CharField(max_length=50)

    class Meta:
        db_table = 'Maladie_chronique'


class Allergie(models.Model):
    cause = models.CharField(max_length=50)

    class Meta:
        db_table = 'Allergie'


class Patient_allergie(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    allergie = models.ForeignKey(Allergie, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Patient_allergie'


class Patient_chronique(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    maladie_chronique = models.ForeignKey('Maladie_chronique', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Patient_chronique'


class Centre_sanitaire(models.Model):
    nom_centre = models.CharField(max_length=50)

    class Meta:
        db_table = 'Centre_sanitaire'


class Agent_centre(models.Model):
    agent_sanitaire = models.ForeignKey(Agent_sanitaire, on_delete=models.CASCADE)
    centre_sanitaire = models.ForeignKey(Centre_sanitaire, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Agent_centre'


class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    agent_centre = models.ForeignKey(Agent_centre, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    traitement = models.TextField()

    class Meta:
        db_table = 'Consultation'




