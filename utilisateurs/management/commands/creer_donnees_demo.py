"""
Commande de gestion pour créer des données de démonstration.
Utilisation: python manage.py creer_donnees_demo
"""

import random
from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from exploitation.models import Exploitation
from parcelles.models import Parcelle
from cultures.models import Culture, Recolte
from activites.models import Activite
from stock.models import Intrant, MouvementStock
from ventes.models import Client, VENTE, VenteArticle
from finances.models import Transaction

User = get_user_model()


class Command(BaseCommand):
    help = 'Crée des données de démonstration pour SmartFarm'

    def handle(self, *args, **options):
        self.stdout.write('Création des données de démonstration...')

        # Créer un utilisateur admin
        self.creer_utilisateurs()

        # Créer des exploitations
        self.creer_exploitations()

        # Créer des parcelles
        self.creer_parcelles()

        # Créer des cultures
        self.creer_cultures()

        # Créer des récoltes
        self.creer_recoltes()

        # Créer des activités
        self.creer_activites()

        # Créer des intrants et mouvements de stock
        self.creer_stock()

        # Créer des clients et ventes
        self.creer_ventes()

        # Créer des transactions financières
        self.creer_transactions()

        self.stdout.write(self.style.SUCCESS('Données de démonstration créées avec succès!'))
        self.stdout.write('')
        self.stdout.write('Comptes créés:')
        self.stdout.write('  - Admin: admin / admin123')
        self.stdout.write('  - Agriculteur: jean / jean123')
        self.stdout.write('  - Gestionnaire: marie / marie123')

    def creer_utilisateurs(self):
        """Crée des utilisateurs de démonstration"""
        self.stdout.write('  Création des utilisateurs...')

        # Admin
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@smartfarm.com',
                'first_name': 'Admin',
                'last_name': 'SmartFarm',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            admin.profil.role = 'admin'
            admin.profil.save()

        # Agriculteur
        jean, created = User.objects.get_or_create(
            username='jean',
            defaults={
                'email': 'jean@smartfarm.com',
                'first_name': 'Jean',
                'last_name': 'Dupont',
            }
        )
        if created:
            jean.set_password('jean123')
            jean.save()
            jean.profil.role = 'agriculteur'
            jean.profil.telephone = '+228 90 00 00 01'
            jean.profil.save()

        # Gestionnaire
        marie, created = User.objects.get_or_create(
            username='marie',
            defaults={
                'email': 'marie@smartfarm.com',
                'first_name': 'Marie',
                'last_name': 'Martin',
            }
        )
        if created:
            marie.set_password('marie123')
            marie.save()
            marie.profil.role = 'gestionnaire'
            marie.profil.telephone = '+228 90 00 00 02'
            marie.profil.save()

    def creer_exploitations(self):
        """Crée des exploitations de démonstration"""
        self.stdout.write('  Création des exploitations...')

        jean = User.objects.get(username='jean')
        marie = User.objects.get(username='marie')

        exploitations = [
            {
                'nom': 'Ferme Maraîchère du Lac',
                'description': 'Exploitation spécialisée dans la culture de légumes biologiques',
                'statut': 'active',
                'responsable': jean,
                'adresse': 'Route de Lomé, Bè, Togo',
                'contact_email': 'ferme.lac@smartfarm.com',
                'contact_telephone': '+228 90 11 11 11',
            },
            {
                'nom': 'Domaine Agricole Savè',
                'description': 'Grande exploitation céréalière et maraîchère',
                'statut': 'active',
                'responsable': marie,
                'adresse': 'Savé, Collines, Togo',
                'contact_email': 'save@smartfarm.com',
                'contact_telephone': '+228 90 22 22 22',
            },
            {
                'nom': 'Jardin Pilote Adidogomé',
                'description': 'Jardin expérimentation pour nouvelles cultures',
                'statut': 'active',
                'responsable': jean,
                'adresse': 'Adidogomé, Lomé, Togo',
                'contact_email': 'pilote@smartfarm.com',
                'contact_telephone': '+228 90 33 33 33',
            },
        ]

        for exp_data in exploitations:
            Exploitation.objects.get_or_create(
                nom=exp_data['nom'],
                defaults=exp_data
            )

    def creer_parcelles(self):
        """Crée des parcelles de démonstration"""
        self.stdout.write('  Création des parcelles...')

        ferme_lac = Exploitation.objects.get(nom='Ferme Maraîchère du Lac')
        domaine_save = Exploitation.objects.get(nom='Domaine Agricole Savè')
        jardin_pilote = Exploitation.objects.get(nom='Jardin Pilote Adidogomé')

        parcelles = [
            # Ferme Lac
            {'nom': 'Parcelle A1', 'code': 'FL-A1', 'superficie': Decimal('2500.00'), 'type_sol': 'limoneux', 'irrigation': True, 'statut': 'actif', 'exploitation': ferme_lac},
            {'nom': 'Parcelle A2', 'code': 'FL-A2', 'superficie': Decimal('1800.00'), 'type_sol': 'sableux', 'irrigation': True, 'statut': 'actif', 'exploitation': ferme_lac},
            {'nom': 'Parcelle B1', 'code': 'FL-B1', 'superficie': Decimal('3200.00'), 'type_sol': 'argileux', 'irrigation': False, 'statut': 'actif', 'exploitation': ferme_lac},
            {'nom': 'Parcelle B2', 'code': 'FL-B2', 'superficie': Decimal('1500.00'), 'type_sol': 'mixte', 'irrigation': True, 'statut': 'en_preparation', 'exploitation': ferme_lac},
            # Domaine Savè
            {'nom': 'Champ C1', 'code': 'DS-C1', 'superficie': Decimal('5000.00'), 'type_sol': 'limoneux', 'irrigation': True, 'statut': 'actif', 'exploitation': domaine_save},
            {'nom': 'Champ C2', 'code': 'DS-C2', 'superficie': Decimal('4500.00'), 'type_sol': 'sableux', 'irrigation': False, 'statut': 'actif', 'exploitation': domaine_save},
            {'nom': 'Champ D1', 'code': 'DS-D1', 'superficie': Decimal('6000.00'), 'type_sol': 'argileux', 'irrigation': True, 'statut': 'actif', 'exploitation': domaine_save},
            # Jardin Pilote
            {'nom': 'Parcelle E1', 'code': 'JP-E1', 'superficie': Decimal('800.00'), 'type_sol': 'organique', 'irrigation': True, 'statut': 'actif', 'exploitation': jardin_pilote},
            {'nom': 'Parcelle E2', 'code': 'JP-E2', 'superficie': Decimal('600.00'), 'type_sol': 'organique', 'irrigation': True, 'statut': 'actif', 'exploitation': jardin_pilote},
        ]

        for par_data in parcelles:
            Parcelle.objects.get_or_create(
                code=par_data['code'],
                defaults=par_data
            )

    def creer_cultures(self):
        """Crée des cultures de démonstration"""
        self.stdout.write('  Création des cultures...')

        parcelles = Parcelle.objects.all()
        today = date.today()

        cultures_data = [
            {'nom': 'Tomate', 'variete': 'Roma', 'duree': 90},
            {'nom': 'Oignon', 'variete': 'Violet de Galmi', 'duree': 120},
            {'nom': 'Piment', 'variete': 'Sankpiti', 'duree': 75},
            {'nom': 'Carotte', 'variete': 'Nantaise', 'duree': 100},
            {'nom': 'Laitue', 'variete': 'Batavia', 'duree': 45},
            {'nom': 'Maïs', 'variete': 'Locale', 'duree': 110},
            {'nom': 'Riz', 'variete': 'NERICA', 'duree': 130},
            {'nom': 'Aubergine', 'variete': 'Black Beauty', 'duree': 80},
        ]

        for i, parcelle in enumerate(parcelles):
            culture_info = cultures_data[i % len(cultures_data)]
            date_semis = today - timedelta(days=random.randint(10, 60))
            date_recolte = date_semis + timedelta(days=culture_info['duree'])

            # Déterminer le statut
            if date_recolte < today:
                statut = random.choice(['recolte', 'terminee'])
            elif date_recolte <= today + timedelta(days=15):
                statut = 'mature'
            else:
                statut = 'en_croissance'

            Culture.objects.get_or_create(
                nom=culture_info['nom'],
                parcelle=parcelle,
                defaults={
                    'variete': culture_info['variete'],
                    'date_semis': date_semis,
                    'date_prevision_recolte': date_recolte,
                    'rendement_attendu': Decimal(str(random.uniform(2.0, 8.0))),
                    'statut': statut,
                    'notes': f"Culture de {culture_info['nom']} variété {culture_info['variete']}",
                }
            )

    def creer_recoltes(self):
        """Crée des récoltes de démonstration"""
        self.stdout.write('  Création des récoltes...')

        cultures_terminees = Culture.objects.filter(statut__in=['recolte', 'terminee'])

        for culture in cultures_terminees:
            # Créer 1 à 3 récoltes par culture
            nb_recoltes = random.randint(1, 3)
            for j in range(nb_recoltes):
                date_recolte = culture.date_semis + timedelta(
                    days=random.randint(30, (culture.date_prevision_recolte - culture.date_semis).days)
                )
                Recolte.objects.get_or_create(
                    culture=culture,
                    date=date_recolte,
                    defaults={
                        'parcelle': culture.parcelle,
                        'quantite': Decimal(str(random.uniform(50.0, 500.0))),
                        'unite': random.choice(['kg', 'panier', 'unite']),
                        'qualite': random.choice(['excellente', 'bonne', 'acceptable']),
                        'notes': f"Récolte #{j+1} de {culture.nom}",
                    }
                )

    def creer_activites(self):
        """Crée des activités de démonstration"""
        self.stdout.write('  Création des activités...')

        jean = User.objects.get(username='jean')
        marie = User.objects.get(username='marie')
        parcelles = Parcelle.objects.all()
        cultures = Culture.objects.all()
        today = date.today()

        activites_data = [
            {'titre': 'Semis de tomates', 'type': 'semis', 'statut': 'terminee'},
            {'titre': 'Irrigation parcelle A1', 'type': 'irrigation', 'statut': 'terminee'},
            {'titre': 'Traitement anti-parasitaire', 'type': 'entretien', 'statut': 'en_cours'},
            {'titre': 'Récolte oignons', 'type': 'recolte', 'statut': 'planifie'},
            {'titre': 'Fertilisation parcelle B1', 'type': 'entretien', 'statut': 'terminee'},
            {'titre': 'Vente au marché', 'type': 'ventes', 'statut': 'terminee'},
            {'titre': 'Transport récolte', 'type': 'transport', 'statut': 'planifie'},
            {'titre': 'Préparation sol parcelle B2', 'type': 'entretien', 'statut': 'en_cours'},
        ]

        for i, act_data in enumerate(activites_data):
            parcelle = parcelles[i % len(parcelles)]
            culture = cultures.filter(parcelle=parcelle).first()

            Activite.objects.get_or_create(
                titre=act_data['titre'],
                defaults={
                    'description': f"Activité: {act_data['titre']}",
                    'type_activite': act_data['type'],
                    'statut': act_data['statut'],
                    'parcelle': parcelle,
                    'culture': culture,
                    'responsable': random.choice([jean, marie]),
                    'date_debut': today - timedelta(days=random.randint(1, 30)),
                    'date_fin': today + timedelta(days=random.randint(1, 15)) if act_data['statut'] == 'planifie' else today - timedelta(days=random.randint(0, 5)),
                }
            )

    def creer_stock(self):
        """Crée des intrants et mouvements de stock de démonstration"""
        self.stdout.write('  Création des intrants et mouvements de stock...')

        jean = User.objects.get(username='jean')

        intrants_data = [
            {'nom': 'Engrais NPK', 'description': 'Engrais composé NPK 15-15-15', 'quantite': Decimal('250.00'), 'unite': 'kg', 'seuil_alerte': Decimal('50.00')},
            {'nom': 'Fongicide Bio', 'description': 'Fongicide biologique pour traitement', 'quantite': Decimal('5.00'), 'unite': 'l', 'seuil_alerte': Decimal('10.00')},
            {'nom': 'Semences Tomates', 'description': 'Semences de tomate Roma', 'quantite': Decimal('500.00'), 'unite': 'unite', 'seuil_alerte': Decimal('100.00')},
            {'nom': 'Herbicide', 'description': 'Herbicide sélectif', 'quantite': Decimal('15.00'), 'unite': 'l', 'seuil_alerte': Decimal('5.00')},
            {'nom': 'Compost', 'description': 'Compost organique', 'quantite': Decimal('1000.00'), 'unite': 'kg', 'seuil_alerte': Decimal('200.00')},
            {'nom': 'Semences Oignons', 'description': 'Semences oignon Violet de Galmi', 'quantite': Decimal('300.00'), 'unite': 'unite', 'seuil_alerte': Decimal('50.00')},
        ]

        for int_data in intrants_data:
            intrant, created = Intrant.objects.get_or_create(
                nom=int_data['nom'],
                defaults=int_data
            )

            # Créer des mouvements de stock
            if created:
                # Entrée initiale
                MouvementStock.objects.create(
                    intrant=intrant,
                    type_mouvement='entree',
                    quantite=int_data['quantite'],
                    date_mouvement=date.today() - timedelta(days=random.randint(10, 30)),
                    responsable=jean,
                    commentaire='Stock initial'
                )

                # Quelques sorties
                if random.choice([True, False]):
                    MouvementStock.objects.create(
                        intrant=intrant,
                        type_mouvement='sortie',
                        quantite=int_data['quantite'] * Decimal('0.2'),
                        date_mouvement=date.today() - timedelta(days=random.randint(1, 10)),
                        responsable=jean,
                        commentaire='Utilisation pour traitement'
                    )

    def creer_ventes(self):
        """Crée des clients et ventes de démonstration"""
        self.stdout.write('  Création des clients et ventes...')

        jean = User.objects.get(username='jean')
        marie = User.objects.get(username='marie')
        cultures = Culture.objects.all()

        clients_data = [
            {'nom': 'Restaurant Le Bon Goût', 'type_client': 'restaurant', 'email': 'contact@bon-gout.tg', 'telephone': '+228 90 44 44 44', 'adresse': 'Centre-ville, Lomé', 'ville': 'Lomé'},
            {'nom': 'Supermarché PriceSmart', 'type_client': 'commerce', 'email': 'achats@pricesmart.tg', 'telephone': '+228 90 55 55 55', 'adresse': 'Bè, Lomé', 'ville': 'Lomé'},
            {'nom': 'Kofi Mensah', 'type_client': 'particulier', 'email': 'kofi@email.com', 'telephone': '+228 90 66 66 66', 'adresse': 'Adidogomé, Lomé', 'ville': 'Lomé'},
            {'nom': 'Entreprise AgriPlus', 'type_client': 'entreprise', 'email': 'info@agriplus.tg', 'telephone': '+228 90 77 77 77', 'adresse': 'Zoned industrielle, Lomé', 'ville': 'Lomé'},
        ]

        for cli_data in clients_data:
            client, created = Client.objects.get_or_create(
                nom=cli_data['nom'],
                defaults=cli_data
            )

            if created:
                # Créer 1 à 2 ventes par client
                for v in range(random.randint(1, 2)):
                    vente = VENTE.objects.create(
                        client=client,
                        description=f"Vente de légumes frais",
                        statut=random.choice(['confirmee', 'livree', 'brouillon']),
                        total=Decimal(str(random.uniform(50000, 500000))),
                        date_commande=date.today() - timedelta(days=random.randint(1, 30)),
                        responsable=random.choice([jean, marie]),
                    )

                    # Ajouter des articles à la vente
                    for culture in cultures[:random.randint(1, 3)]:
                        VenteArticle.objects.create(
                            vente=vente,
                            culture=culture,
                            parcelle=culture.parcelle,
                            quantite=Decimal(str(random.uniform(10, 100))),
                            prix_unitaire=Decimal(str(random.uniform(500, 2000))),
                        )

    def creer_transactions(self):
        """Crée des transactions financières de démonstration"""
        self.stdout.write('  Création des transactions financières...')

        jean = User.objects.get(username='jean')
        marie = User.objects.get(username='marie')

        # Recettes
        recettes = [
            {'titre': 'Vente tomates', 'montant': Decimal('150000.00'), 'categorie': 'vente'},
            {'titre': 'Vente oignons', 'montant': Decimal('200000.00'), 'categorie': 'vente'},
            {'titre': 'Subvention agricole', 'montant': Decimal('500000.00'), 'categorie': 'subvention'},
            {'titre': 'Vente piments', 'montant': Decimal('75000.00'), 'categorie': 'vente'},
            {'titre': 'Vente carottes', 'montant': Decimal('120000.00'), 'categorie': 'vente'},
        ]

        for rec_data in recettes:
            Transaction.objects.get_or_create(
                titre=rec_data['titre'],
                defaults={
                    'type_transaction': 'recette',
                    'description': f"Recette: {rec_data['titre']}",
                    'montant': rec_data['montant'],
                    'categorie': rec_data['categorie'],
                    'date_operation': date.today() - timedelta(days=random.randint(1, 60)),
                    'responsable': random.choice([jean, marie]),
                }
            )

        # Dépenses
        depenses = [
            {'titre': 'Achat engrais', 'montant': Decimal('80000.00'), 'categorie': 'achat'},
            {'titre': 'Salaires ouvriers', 'montant': Decimal('300000.00'), 'categorie': 'salaires'},
            {'titre': 'Entretien équipement', 'montant': Decimal('45000.00'), 'categorie': 'entretien'},
            {'titre': 'Achat semences', 'montant': Decimal('60000.00'), 'categorie': 'achat'},
            {'titre': 'Facture électricité', 'montant': Decimal('35000.00'), 'categorie': 'autre'},
            {'titre': 'Transport marchandises', 'montant': Decimal('25000.00'), 'categorie': 'autre'},
        ]

        for dep_data in depenses:
            Transaction.objects.get_or_create(
                titre=dep_data['titre'],
                defaults={
                    'type_transaction': 'depense',
                    'description': f"Dépense: {dep_data['titre']}",
                    'montant': dep_data['montant'],
                    'categorie': dep_data['categorie'],
                    'date_operation': date.today() - timedelta(days=random.randint(1, 60)),
                    'responsable': random.choice([jean, marie]),
                }
            )