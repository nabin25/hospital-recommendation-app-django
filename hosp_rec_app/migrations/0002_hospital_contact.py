# Generated by Django 4.2 on 2023-05-01 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosp_rec_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='contact',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
