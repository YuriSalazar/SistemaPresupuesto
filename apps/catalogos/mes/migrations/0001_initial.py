# Generated by Django 5.1.1 on 2024-09-24 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=2, unique=True, verbose_name='Codigo')),
                ('descripcion', models.CharField(max_length=50, verbose_name='Descripcion')),
            ],
            options={
                'verbose_name_plural': 'Meses',
            },
        ),
    ]
