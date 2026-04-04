from django.db import migrations


def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name='Manager')
    Group.objects.get_or_create(name='Delivery crew')


def reverse_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Manager', 'Delivery crew']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('JoesDeliDRF', '0007_joesdeli_seed_menu'),
    ]

    operations = [
        migrations.RunPython(create_groups, reverse_groups),
    ]
