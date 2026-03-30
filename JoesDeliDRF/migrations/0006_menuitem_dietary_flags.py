from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JoesDeliDRF', '0005_menuitem_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='is_vegetarian',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='is_vegan',
            field=models.BooleanField(default=False),
        ),
    ]
