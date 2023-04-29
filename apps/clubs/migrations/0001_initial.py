# Generated by Django 4.2 on 2023-04-29 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('championship', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=127)),
                ('image', models.ImageField(upload_to='clubs')),
                ('coach', models.CharField(max_length=127)),
                ('championship', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='club', to='championship.championship')),
            ],
        ),
    ]
