# Generated by Django 4.1.7 on 2023-05-17 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dziennik', '0005_remove_rodzic_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='ocena',
            name='kategoria',
            field=models.TextField(default='sprawdzian', max_length=30),
        ),
        migrations.AddField(
            model_name='uczen',
            name='nr_dziennik',
            field=models.IntegerField(default=0),
        ),
    ]
