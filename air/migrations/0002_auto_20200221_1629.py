# Generated by Django 3.0.3 on 2020-02-21 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('air', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='is_question',
            new_name='is_answer',
        ),
    ]