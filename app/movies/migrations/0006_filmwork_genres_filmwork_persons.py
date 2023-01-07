# Generated by Django 4.0.4 on 2022-12-08 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_auto_20221129_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(related_name='filmworks', through='movies.GenreFilmwork', to='movies.genre', verbose_name='Genres'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(related_name='filmworks', through='movies.PersonFilmwork', to='movies.person', verbose_name='Persons'),
        ),
    ]
