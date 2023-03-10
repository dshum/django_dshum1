# Generated by Django 4.1.7 on 2023-02-26 17:36

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='token',
            options={},
        ),
        migrations.AlterModelManagers(
            name='token',
            managers=[
                ('tokens', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='token',
            name='full_url',
            field=models.URLField(max_length=1000, unique=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='short_url',
            field=models.CharField(db_index=True, max_length=20, unique=True),
        ),
    ]
