# Generated by Django 3.2 on 2023-02-07 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APImesin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mesin',
            name='id_pengguna_aktif',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
    ]