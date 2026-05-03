import re

from django.db import migrations, models


def split_mileage(apps, schema_editor):
    Car = apps.get_model('web', 'Car')
    for car in Car.objects.all():
        raw_mileage = str(car.mileage or '')
        unit = 'km' if 'km' in raw_mileage.lower() else 'mil'
        digits = re.sub(r'\D', '', raw_mileage)
        car.mileage = int(digits) if digits else 0
        car.mileage_unit = unit
        car.save(update_fields=['mileage', 'mileage_unit'])


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_teammember_telegram_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='mileage_unit',
            field=models.CharField(choices=[('km', 'km'), ('mil', 'mil')], default='mil', max_length=3),
        ),
        migrations.RunPython(split_mileage, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='car',
            name='mileage',
            field=models.PositiveIntegerField(),
        ),
    ]
