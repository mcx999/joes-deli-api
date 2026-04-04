from django.db import migrations


def rename_delivery_crew(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name='Delivery crew').update(name='DeliveryCrew')


def reverse_rename_delivery_crew(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name='DeliveryCrew').update(name='Delivery crew')


class Migration(migrations.Migration):

    dependencies = [
        ('JoesDeliDRF', '0008_create_groups'),
    ]

    operations = [
        migrations.RunPython(rename_delivery_crew, reverse_rename_delivery_crew),
    ]
