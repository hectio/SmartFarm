# Déploiement SmartFarm

## Variables obligatoires en production

Définir les variables d'environnement suivantes avant de lancer Django :

```text
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=<clé longue et aléatoire>
DJANGO_ALLOWED_HOSTS=smartfarm.tg,www.smartfarm.tg
DJANGO_CSRF_TRUSTED_ORIGINS=https://smartfarm.tg,https://www.smartfarm.tg
```

Avec `DJANGO_DEBUG=False`, les cookies sécurisés et HSTS sont activés par défaut.
Le serveur doit être placé derrière HTTPS. Les paramètres `DJANGO_*` peuvent
être ajustés si le proxy inverse gère déjà la redirection HTTPS.

En développement local, conserver `DJANGO_DEBUG=True` et utiliser les valeurs
de [.env.example](.env.example).

Avant la mise en ligne :

```text
python manage.py check --deploy
python manage.py collectstatic --noinput
```