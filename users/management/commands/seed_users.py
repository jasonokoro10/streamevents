# seed_users.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from faker import Faker
import re

User = get_user_model()
fake = Faker('es_ES')  # Configuració de Faker amb locale es_ES

class Command(BaseCommand):
    help = '🌱 Crea usuaris de prova per al desenvolupament'

    def add_arguments(self, parser):
        """Defineix els arguments opcionals del comandament"""
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Nombre d\'usuaris a crear'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Elimina tots els usuaris existents abans de crear-ne de nous'
        )
        parser.add_argument('--with-follows', action='store_true', default=False, help='Crea relacions de seguiment aleatòries')
    
    def handle(self, *args, **options):
        """Lògica principal del comandament"""
        
        # Comprova si s'ha de netejar la base de dades d'usuaris existents
        if options['clear']:
            self.stdout.write('🗑️  Eliminant usuaris existents...')
            count = 0
            for user in User.objects.all():
                if not user.is_superuser:
                    user.delete()
                    count += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Eliminats {count} usuaris')
            )
        
        # Obté el nombre d'usuaris a crear des de l'argument --users
        num_users = options['users']
        with transaction.atomic():
            
            # Crear grups si no existeixen
            groups = self.create_groups()
            
            # Crear usuaris
            users_created = self.create_users(num_users, groups)
            
        self.stdout.write(
            self.style.SUCCESS(f'✅ {users_created} usuaris creats correctament!')
        )
   
    def create_groups(self):
        """Crea els grups necessaris"""
        group_names = ['Organitzadors', 'Participants', 'Moderadors']
        groups = {}
        
        for name in group_names:
            group, created = Group.objects.get_or_create(name=name)
            groups[name] = group
            if created:
                self.stdout.write(f'  ✓ Grup "{name}" creat')
        
        return groups
    
    def clean_username(self, first_name, last_name, index):
        """Neteja accents i caràcters especials, assegura unicitat sense unidecode"""
        
        # Converteix a minúscules i substitueix accents manualment
        accent_map = {
            'àáâãäå': 'a', 'èéêë': 'e', 'ìíîï': 'i',
            'òóôõö': 'o', 'ùúûü': 'u', 'ñ': 'n', 'ç': 'c'
        }
        base_name = f"{first_name}.{last_name}{index}".lower()
        for accents, replacement in accent_map.items():
            for accent in accents:
                base_name = base_name.replace(accent, replacement)
        
        # Elimina caràcters especials, deixant només lletres, números i punts
        username = re.sub(r'[^a-z0-9.]', '', base_name)
        
        # Comprova unicitat
        original_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1
        return username
    
    def create_users(self, num_users, groups):
        """Crea usuaris de prova"""
        users_created = 0
        
        # Crear un admin si no existeix
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@streamevents.com',
                'first_name': 'Admin',
                'last_name': 'Sistema',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            # Assigna display_name amb emoji per a l'admin
            admin.display_name = '🔧 Administrador'  # Assumim que display_name és un camp personalitzat
            admin.save()
            self.stdout.write('  ✓ Superusuari admin creat')
            users_created += 1
            
        # Crear usuaris normals amb faker
        for i in range(1, num_users + 1):
            first_name = fake.first_name()
            last_name = fake.last_name()
            index = i  # Per assegurar unicitat
            
            username = self.clean_username(first_name, last_name, index)
            email = f"{username}@streamevents.com"
            
            # Determinar el rol segons el requisit (cada 5è Organitzador, cada 3è Moderador)
            if i % 5 == 0:
                group = groups['Organitzadors']
                role_emoji = '🎯'
                role = 'org'
            elif i % 3 == 0 and i % 5 != 0:  # Evita solapament amb els múltiples de 5
                group = groups['Moderadors']
                role_emoji = '🛡️'
                role = 'mod'
            else:
                group = groups['Participants']
                role_emoji = ''  # Sense emoji per a Participants
                role = 'part'
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'is_active': True,
                }
            )
            
            if created:
                user.set_password('password123')
                user.groups.add(group)
                # Assigna display_name amb emoji segons rol
                user.display_name = f"{role_emoji} {first_name} {last_name}"  # Assumim camp personalitzat
                # Assigna bio
                user.bio = f"{fake.sentence()} {role.capitalize()} d'esdeveniments en streaming, m'encanta la tecnologia..."
                user.save()
                users_created += 1
                self.stdout.write(f'  ✓ Usuari {username} ({role}) creat')
        
        return users_created
