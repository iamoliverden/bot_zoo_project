# Generated by Django 5.1.3 on 2024-11-17 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zoomzoombotbot_app', '0006_remove_question_answers_answer_animal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]