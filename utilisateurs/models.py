from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class ProfilUtilisateur(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('agriculteur', 'Agriculteur'),
        ('gestionnaire', 'Gestionnaire'),
        ('consultant', 'Consultant'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='agriculteur')
    exploitation = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='utilisateurs/photos/', blank=True, null=True)

    def __str__(self):
        return f"Profil de {self.user.username}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfilUtilisateur.objects.create(user=instance)
    else:
        if hasattr(instance, 'profil'):
            instance.profil.save()
