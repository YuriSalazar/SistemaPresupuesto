# Generated by Django 4.2 on 2024-11-26 03:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movimientoscuenta', '0002_alter_detallemovimientocuenta_movimientocuenta'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detallemovimientocuenta',
            old_name='movimientoCuenta',
            new_name='movimientocuenta',
        ),
    ]
