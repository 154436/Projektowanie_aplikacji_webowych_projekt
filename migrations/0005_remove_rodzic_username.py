# Generated by Django 4.1.7 on 2023-04-19 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dziennik', '0004_nauczyciel_user_uczen_user_alter_nauczyciel_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rodzic',
            name='username',
        ),
    ]
