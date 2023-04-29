# Generated by Django 4.2 on 2023-04-29 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(default=None)),
                ('tour', models.PositiveIntegerField()),
                ('away_gols', models.IntegerField(default=None)),
                ('home_gols', models.IntegerField(default=None)),
                ('away_club', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='match_away', to='clubs.club')),
                ('home_club', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='match_home', to='clubs.club')),
            ],
        ),
    ]
