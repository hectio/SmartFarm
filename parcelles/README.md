# Application Parcelles - SmartFarm

## Vue d'ensemble

L'application **Parcelles** gère les parcelles agricoles du système SmartFarm. Chaque parcelle est une surface de terrain cultivable appartenant à une exploitation.

## Structure

### Répertoire: `parcelles/`

```
parcelles/
├── __init__.py              # Initialisation du paquet
├── admin.py                 # Configuration admin
├── apps.py                  # Configuration de l'application
├── forms.py                 # Formulaires Django
├── models.py                # Modèles de données
├── tests.py                 # Tests unitaires
├── urls.py                  # Routes URL
├── views.py                 # Vues CRUD
└── migrations/
    └── __init__.py
```

### Répertoire: `static/parcelles/`

```
static/parcelles/
├── css/
│   └── parcelles.css        # Styles CSS personnalisés
├── js/
│   └── parcelles.js         # JavaScript interactif
└── images/                  # Dossier pour les images
```

### Répertoire: `templates/parcelles/`

```
templates/parcelles/
├── liste.html               # Liste des parcelles
├── ajouter.html             # Formulaire d'ajout
├── modifier.html            # Formulaire de modification
├── detail.html              # Détails d'une parcelle
└── supprimer.html           # Confirmation de suppression
```

## Modèle Parcelle

### Champs

- **id**: Identifiant unique (auto-généré)
- **nom**: Nom/identifiant de la parcelle
- **code**: Code unique de la parcelle
- **superficie**: Superficie en m² ou hectares
- **type_sol**: Type de sol (choix multiples)
- **latitude**: Latitude GPS (optionnel)
- **longitude**: Longitude GPS (optionnel)
- **description**: Description détaillée
- **statut**: Statut actuel (actif, en_preparation, reposante, suspendu)
- **exploitation**: Référence à l'exploitation (ForeignKey)
- **date_creation**: Date de création
- **date_modification**: Date de dernière modification

### Choices

**Type de sol:**
- argileux
- sableux
- limoneux
- calcaire
- organique
- mixte

**Statut:**
- actif
- en_preparation
- reposante
- suspendu

## Vues CRUD

### ParcelleListView
- URL: `/parcelles/`
- Méthode: GET
- Fonction: Affiche la liste de toutes les parcelles avec filtrage
- Filtres: statut, exploitation, recherche (nom/code)
- Pagination: 20 parcelles par page

### ParcelleDetailView
- URL: `/parcelles/<id>/`
- Méthode: GET
- Fonction: Affiche les détails complets d'une parcelle

### ParcelleCreateView
- URL: `/parcelles/ajouter/`
- Méthode: GET, POST
- Fonction: Crée une nouvelle parcelle
- Redirection: Liste des parcelles après création

### ParcelleUpdateView
- URL: `/parcelles/<id>/modifier/`
- Méthode: GET, POST
- Fonction: Modifie une parcelle existante
- Redirection: Liste des parcelles après modification

### ParcelleDeleteView
- URL: `/parcelles/<id>/supprimer/`
- Méthode: GET, POST
- Fonction: Supprime une parcelle avec confirmation
- Redirection: Liste des parcelles après suppression

## Formulaire

### ParcelleForm

Formulaire Django avec les champs suivants:
- nom
- code
- superficie
- type_sol
- latitude
- longitude
- description
- statut
- exploitation

Les champs sont pré-stylisés avec les classes Bootstrap.

## Administration

L'interface d'administration Django est configurée pour:
- Afficher: code, nom, exploitation, type_sol, statut, superficie, date_creation
- Filtrer par: statut, type_sol, exploitation, date_creation
- Rechercher par: code, nom, description
- Champs en lecture seule: date_creation, date_modification

## Routes URL

| Methode | URL | Vue | Nom |
|---------|-----|-----|-----|
| GET | `/parcelles/` | ParcelleListView | `parcelles:parcelle_list` |
| GET/POST | `/parcelles/ajouter/` | ParcelleCreateView | `parcelles:parcelle_create` |
| GET | `/parcelles/<id>/` | ParcelleDetailView | `parcelles:parcelle_detail` |
| GET/POST | `/parcelles/<id>/modifier/` | ParcelleUpdateView | `parcelles:parcelle_update` |
| GET/POST | `/parcelles/<id>/supprimer/` | ParcelleDeleteView | `parcelles:parcelle_delete` |

## JavaScript

Le fichier `static/parcelles/js/parcelles.js` fournit:

- `confirmDelete(parcelleNom)`: Confirmation avant suppression
- `resetFilters()`: Réinitialisation des filtres
- `validateParcelleForm(formElement)`: Validation du formulaire
- `getSelectedParcellesIds()`: Récupération des IDs sélectionnées

## CSS

Le fichier `static/parcelles/css/parcelles.css` fournit:

- Styles pour les cartes de parcelles
- Badges pour les statuts
- Formulaires personnalisés
- Animations fluides
- Responsive design

## Installation & Migration

1. Les migrations doivent être créées:
   ```bash
   python manage.py makemigrations parcelles
   python manage.py migrate parcelles
   ```

2. Créer un superutilisateur pour l'admin:
   ```bash
   python manage.py createsuperuser
   ```

3. Accéder à l'admin Django:
   - URL: `/admin/`
   - Ajouter des exploitations et des parcelles

## Intégration

- L'app est enregistrée dans `INSTALLED_APPS` dans `config/settings.py`
- Les URLs sont incluses dans `config/urls.py` sous le préfixe `/parcelles/`
- Les templates utilisent la base `base.html` du projet
- Les modèles s'intègrent avec le modèle `Exploitation`

## Notes de développement

- Le modèle `Exploitation` doit être créé dans l'app `exploitation`
- Les tests unitaires de base sont fournis dans `tests.py`
- Les templates sont entièrement intégrés avec Bootstrap 5
- Les messages utilisateur sont affichés via Django messages framework

## Améliorations futures

- Intégration de cartes Google Maps/Leaflet
- Galerie d'images pour les parcelles
- Historique des activités
- Exports CSV/Excel
- API REST pour mobile
- Intégration avec cultures et activités
