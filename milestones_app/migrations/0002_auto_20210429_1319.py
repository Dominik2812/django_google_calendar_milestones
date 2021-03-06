# Generated by Django 3.1.3 on 2021-04-29 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('milestones_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestone',
            name='end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='g_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='start',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='text',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
    ]
