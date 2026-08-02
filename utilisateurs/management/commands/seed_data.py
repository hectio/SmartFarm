import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils import timezone

from faker import Faker

from exploitation.models import Exploitation
from parcelles.models import Parcelle
from cultures.models import Culture, Recolte
from activites.models import Activite
from stock.models import Intrant, MouvementStock
from ventes.models import Client, VENTE, VenteArticle
from finances.models import Transaction
from utilisateurs.models import ProfilUtilisateur

User = get_user_model()

COUNTRY = 'Togo'
REGIONS = [
    'Lomé', 'Sokodé', 'Kara', 'Savanes', 'Plateaux', 'Centrale', 'Maritime', 'Centrale', 'Centrale'
]
SOL_TYPES = ['argileux', 'sableux', 'limoneux', 'calcaire', 'organique', 'mixte']
PARCEL_STATUS = ['actif', 'en_preparation', 'reposante', 'suspendu']
EXPLOITATION_STATUS = ['active', 'inactive', 'suspendue']
CULTURE_STATUS = ['en_croissance', 'mature', 'recolte', 'terminee']
ACTIVITE_TYPES = ['semis', 'entretien', 'irrigation', 'recolte', 'ventes', 'transport', 'autre']
ACTIVITE_STATUS = ['planifie', 'en_cours', 'terminee', 'annulee']
CLIENT_TYPES = ['restaurant', 'commerce', 'particulier', 'entreprise']
VENTE_STATUS = ['brouillon', 'confirmee', 'livree', 'annulee']
INTRANT_UNITS = ['kg', 'g', 'l', 'unite', 'm2', 'm3']
TRANSACTION_TYPES = ['recette', 'depense']
TRANSACTION_CATEGORIES = ['vente', 'subvention', 'achat', 'salaires', 'entretien', 'autre']

LOME_LAT, LOME_LNG = 6.1768, 1.2315


class Command(BaseCommand):
    help = 'Génère des données de démonstration cohérentes pour SmartFarm'

    def handle(self, *args, **kwargs):
        fake = Faker('fr_FR')
        self.stdout.write(self.style.NOTICE('Début du seed de données SmartFarm...'))

        self.clear_data()
        users = self.create_users(fake)
        exploitations = self.create_exploitations(fake, users)
        parcelles = self.create_parcelles(fake, exploitations)
        cultures = self.create_cultures(fake, parcelles)
        recoltes = self.create_recoltes(fake, cultures)
        activites = self.create_activites(fake, parcelles, cultures, users)
        intrants = self.create_intrants(fake)
        self.create_stock_movements(fake, intrants, users)
        clients = self.create_clients(fake)
        ventes = self.create_ventes(fake, clients, cultures, parcelles, users)
        self.create_transactions(fake, ventes)

        self.stdout.write(self.style.SUCCESS('Seed terminé.'))

    def clear_data(self):
        Transaction.objects.all().delete()
        VenteArticle.objects.all().delete()
        VENTE.objects.all().delete()
        Client.objects.all().delete()
        MouvementStock.objects.all().delete()
        Intrant.objects.all().delete()
        Activite.objects.all().delete()
        Recolte.objects.all().delete()
        Culture.objects.all().delete()
        Parcelle.objects.all().delete()
        Exploitation.objects.all().delete()
        ProfilUtilisateur.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()
        self.stdout.write('Données existantes supprimées.')

    def create_users(self, fake):
        users = []
        responsibles = []
        for i in range(8):
            username = f'user_{i+1}'
            user = User.objects.create_user(
                username=username,
                email=f'{username}@smartfarm.local',
                password='SmartFarm123!'
            )
            user.first_name = fake.first_name()
            user.last_name = fake.last_name()
            user.save()
            profile = user.profil
            profile.telephone = fake.phone_number()
            profile.adresse = fake.address()
            profile.role = random.choice(['agriculteur', 'gestionnaire', 'consultant'])
            profile.exploitation = fake.city()
            profile.save()
            users.append(user)
            responsibles.append(user)
        self.stdout.write(f'{len(users)} utilisateurs créés.')
        return responsibles

    def create_exploitations(self, fake, users):
        exploitations = []
        noms = [
            'Ferme de la Mango',
            'Domaine AgriTogo',
            'Plantation Kpalimé',
            'Exploitation Lomé Sud',
            'Ferme du Plateau'
        ]
        for idx, nom in enumerate(noms):
            explo = Exploitation.objects.create(
                nom=nom,
                description=fake.paragraph(nb_sentences=3),
                statut=random.choice(EXPLOITATION_STATUS),
                responsable=random.choice(users),
                adresse=f'{fake.building_number()} {fake.street_name()}, {random.choice(REGIONS)}, {COUNTRY}',
                contact_email=f'contact{idx+1}@{nom.replace(" ", "").lower()}.tg',
                contact_telephone=f'+228{fake.random_number(digits=8, fix_len=True)}'
            )
            exploitations.append(explo)
        self.stdout.write(f'{len(exploitations)} exploitations créées.')
        return exploitations

    def create_parcelles(self, fake, exploitations):
        parcelles = []
        code_index = 1
        for exploitation in exploitations:
            for j in range(3, 5):
                nom = f'Parcelle {chr(65 + code_index)}'
                code = f'PARC-{code_index:03d}'
                lat = LOME_LAT + fake.random.uniform(-0.4, 0.4)
                lng = LOME_LNG + fake.random.uniform(-0.4, 0.4)
                parcelle = Parcelle.objects.create(
                    nom=nom,
                    code=code,
                    superficie=round(fake.random.uniform(0.8, 6.5), 2),
                    type_sol=random.choice(SOL_TYPES),
                    irrigation=fake.boolean(chance_of_getting_true=35),
                    latitude=round(lat, 6),
                    longitude=round(lng, 6),
                    description=fake.sentence(nb_words=10),
                    statut=random.choice(PARCEL_STATUS),
                    exploitation=exploitation,
                )
                parcelles.append(parcelle)
                code_index += 1
        self.stdout.write(f'{len(parcelles)} parcelles créées.')
        return parcelles

    def create_cultures(self, fake, parcelles):
        cultures = []
        culture_types = [
            ('Maïs', 'Hybryd'),
            ('Tomate', 'Cherry'),
            ('Igname', 'Blanche'),
            ('Banane', 'Plantain'),
            ('Arachide', 'Grain'),
            ('Café', 'Arabica'),
            ('Mangue', 'Kent')
        ]
        for parcelle in parcelles:
            nb = random.randint(1, 2)
            for _ in range(nb):
                nom, variete = random.choice(culture_types)
                date_semis = fake.date_between(start_date='-120d', end_date='-20d')
                duree = random.randint(60, 140)
                date_recolte = date_semis + timedelta(days=duree)
                culture = Culture.objects.create(
                    nom=nom,
                    variete=variete,
                    parcelle=parcelle,
                    date_semis=date_semis,
                    date_prevision_recolte=date_recolte,
                    rendement_attendu=round(random.uniform(1.0, 6.0), 2),
                    statut=random.choice(CULTURE_STATUS),
                    notes=fake.sentence(nb_words=8)
                )
                cultures.append(culture)
        self.stdout.write(f'{len(cultures)} cultures créées.')
        return cultures

    def create_recoltes(self, fake, cultures):
        recoltes = []
        for culture in cultures:
            if culture.statut in ['mature', 'recolte']:
                quantite = round(random.uniform(100, 1200), 2)
                recolte = Recolte.objects.create(
                    date=fake.date_between(start_date=culture.date_semis, end_date=culture.date_prevision_recolte),
                    culture=culture,
                    parcelle=culture.parcelle,
                    quantite=quantite,
                    unite='kg',
                    qualite=random.choice(['bonne', 'excellente', 'acceptable']),
                    notes=fake.sentence(nb_words=6)
                )
                recoltes.append(recolte)
        self.stdout.write(f'{len(recoltes)} récoltes créées.')
        return recoltes

    def create_activites(self, fake, parcelles, cultures, users):
        activites = []
        for parcelle in parcelles:
            for _ in range(random.randint(1, 3)):
                culture = random.choice(cultures)
                if culture.parcelle != parcelle:
                    culture = random.choice([c for c in cultures if c.parcelle == parcelle] or [culture])
                debut = fake.date_between(start_date='-40d', end_date='+20d')
                fin = debut + timedelta(days=random.randint(1, 12))
                activite = Activite.objects.create(
                    titre=fake.sentence(nb_words=4),
                    description=fake.sentence(nb_words=10),
                    type_activite=random.choice(ACTIVITE_TYPES),
                    statut=random.choice(ACTIVITE_STATUS),
                    parcelle=parcelle,
                    culture=culture,
                    responsable=random.choice(users),
                    date_debut=debut,
                    date_fin=fin,
                )
                activites.append(activite)
        self.stdout.write(f'{len(activites)} activités créées.')
        return activites

    def create_intrants(self, fake):
        intrants = []
        types = ['Engrais', 'Pesticide', 'Semences', 'Carburant', 'Fertilisant', 'Filet']
        for nom in types:
            intrant = Intrant.objects.create(
                nom=nom,
                description=fake.sentence(nb_words=8),
                quantite=round(random.uniform(25, 450), 2),
                unite=random.choice(INTRANT_UNITS),
                seuil_alerte=round(random.uniform(10, 60), 2)
            )
            intrants.append(intrant)
        self.stdout.write(f'{len(intrants)} intrants créés.')
        return intrants

    def create_stock_movements(self, fake, intrants, users):
        mouvements = []
        for intrant in intrants:
            for _ in range(random.randint(1, 3)):
                quantite = round(random.uniform(5, 120), 2)
                mouvement = MouvementStock.objects.create(
                    intrant=intrant,
                    type_mouvement=random.choice(['entree', 'sortie']),
                    quantite=quantite,
                    date_mouvement=fake.date_between(start_date='-120d', end_date='today'),
                    responsable=random.choice(users),
                    commentaire=fake.sentence(nb_words=7)
                )
                mouvements.append(mouvement)
        self.stdout.write(f'{len(mouvements)} mouvements de stock créés.')
        return mouvements

    def create_clients(self, fake):
        clients = []
        for _ in range(10):
            client = Client.objects.create(
                nom=fake.company() if random.choice([True, False]) else fake.name(),
                type_client=random.choice(CLIENT_TYPES),
                email=fake.company_email(),
                telephone=f'+228{fake.random_number(digits=8, fix_len=True)}',
                adresse=fake.address(),
                code_postal=str(fake.random_number(digits=5, fix_len=True)),
                ville=random.choice(REGIONS)
            )
            clients.append(client)
        self.stdout.write(f'{len(clients)} clients créés.')
        return clients

    def create_ventes(self, fake, clients, cultures, parcelles, users):
        ventes = []
        for _ in range(12):
            date_commande = fake.date_between(start_date='-90d', end_date='today')
            client = random.choice(clients)
            vente = VENTE.objects.create(
                client=client,
                description=fake.sentence(nb_words=10),
                statut=random.choice(VENTE_STATUS),
                total=0,
                date_commande=date_commande,
                responsable=random.choice(users)
            )
            lignes = []
            for _ in range(random.randint(1, 3)):
                culture = random.choice(cultures)
                parcelle = culture.parcelle
                quantite = round(random.uniform(10, 120), 2)
                prix = round(random.uniform(150, 420), 2)
                article = VenteArticle.objects.create(
                    vente=vente,
                    culture=culture,
                    parcelle=parcelle,
                    quantite=quantite,
                    prix_unitaire=prix
                )
                lignes.append(article)
                vente.total += article.montant_total()
            vente.save()
            ventes.append(vente)
        self.stdout.write(f'{len(ventes)} ventes créées.')
        return ventes

    def create_transactions(self, fake, ventes):
        transactions = []
        for vente in ventes:
            transaction = Transaction.objects.create(
                type_transaction='recette',
                titre=f'Recette vente #{vente.pk}',
                description=f'Paiement de la vente {vente.pk}',
                montant=vente.total,
                categorie='vente',
                date_operation=vente.date_commande,
                responsable=vente.responsable
            )
            transactions.append(transaction)

        for _ in range(8):
            depense = Transaction.objects.create(
                type_transaction='depense',
                titre=f'Dépense {fake.word().capitalize()}',
                description=fake.sentence(nb_words=8),
                montant=round(random.uniform(120, 760), 2),
                categorie=random.choice(['achat', 'salaires', 'entretien', 'autre']),
                date_operation=fake.date_between(start_date='-90d', end_date='today'),
                responsable=random.choice(User.objects.exclude(is_superuser=True))
            )
            transactions.append(depense)
        self.stdout.write(f'{len(transactions)} transactions créées.')
        return transactions
