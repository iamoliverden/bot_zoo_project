# Generated by Django 5.1.3 on 2024-11-17 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zoomzoombotbot_app', '0002_delete_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='animal',
            old_name='answers',
            new_name='answer',
        ),
        migrations.RenameField(
            model_name='animal',
            old_name='animal',
            new_name='picture',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='answers',
            new_name='answer',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
