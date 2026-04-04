from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


ROLE_USERS = [
    {
        'username': 'admin_joe',
        'password': 'admin123',
        'email': 'admin@joesdeli.com',
        'is_staff': True,
        'is_superuser': True,
        'group': None,
    },
    {
        'username': 'manager_joe',
        'password': 'manager123',
        'email': 'manager@joesdeli.com',
        'group': 'Manager',
    },
    {
        'username': 'crew_joe',
        'password': 'crew123',
        'email': 'crew@joesdeli.com',
        'group': 'DeliveryCrew',
    },
    {
        'username': 'customer_joe',
        'password': 'customer123',
        'email': 'customer@joesdeli.com',
        'group': None,
    },
]


class Command(BaseCommand):
    help = 'Create dev test users for each role: Admin, Manager, DeliveryCrew, Customer'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete and recreate existing test users',
        )

    def handle(self, *args, **options):
        manager_group, _ = Group.objects.get_or_create(name='Manager')
        crew_group, _ = Group.objects.get_or_create(name='DeliveryCrew')
        groups = {'Manager': manager_group, 'DeliveryCrew': crew_group}

        for spec in ROLE_USERS:
            group_name = spec.get('group')
            username = spec['username']

            if options['reset']:
                User.objects.filter(username=username).delete()

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': spec.get('email', ''),
                    'is_staff': spec.get('is_staff', False),
                    'is_superuser': spec.get('is_superuser', False),
                },
            )

            if created:
                user.set_password(spec['password'])
                user.save()
                if group_name:
                    user.groups.add(groups[group_name])
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  Created  {username:<20} role={group_name or 'Customer'}"
                        f"  password={spec['password']}"
                    )
                )
            else:
                self.stdout.write(
                    f"  Skipped  {username:<20} (already exists — use --reset to recreate)"
                )
