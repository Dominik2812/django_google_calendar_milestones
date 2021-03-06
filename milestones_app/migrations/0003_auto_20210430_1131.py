# Generated by Django 3.1.3 on 2021-04-30 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('milestones_app', '0002_auto_20210429_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='color_id',
            field=models.CharField(default='0', max_length=3),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='goal',
            field=models.ForeignKey(blank=True, db_column='goal', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='milestones', to='milestones_app.milestone'),
        ),
    ]
