# Generated by Django 5.1.3 on 2024-11-17 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zoomzoombotbot_app', '0004_answer_testresult_remove_animal_answer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='test_result',
        ),
        migrations.RemoveField(
            model_name='animal',
            name='test_result',
        ),
        migrations.DeleteModel(
            name='TestResult',
        ),
    ]
