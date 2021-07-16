# Generated by Django 3.1.3 on 2021-05-01 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('milestones_app', '0003_auto_20210430_1131'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='milestone',
            name='goal',
            field=models.ForeignKey(blank=True, db_column='goal', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='milestones', to='milestones_app.goal'),
        ),
    ]
