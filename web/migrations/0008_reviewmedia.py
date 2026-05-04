from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_car_mileage_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_type', models.CharField(choices=[('image', 'Image'), ('video', 'Video')], max_length=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='reviews/photos/')),
                ('video', models.FileField(blank=True, null=True, upload_to='reviews/videos/')),
                ('caption', models.CharField(blank=True, max_length=160)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media', to='web.review')),
            ],
            options={
                'ordering': ['sort_order', 'created_at'],
            },
        ),
    ]
