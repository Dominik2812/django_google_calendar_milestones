# Generated by Django 3.1.3 on 2021-05-03 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('milestones_app', '0011_auto_20210502_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='color_code',
            field=models.CharField(default='#039be5', max_length=33),
        ),
        migrations.AddField(
            model_name='milestone',
            name='color_code',
            field=models.CharField(default='#039be5', max_length=3),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='text',
            field=models.TextField(blank=True, default='Why I chose this to be my first Milestone: ...... ---- Is it feasible within the given time span?', max_length=2000, null=True),
        ),
    ]
