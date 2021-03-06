# Generated by Django 2.1.3 on 2018-11-24 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchingapp', '0003_remove_hobby_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='match_requests',
            field=models.ManyToManyField(to='matchingapp.Member'),
        ),
        migrations.AddField(
            model_name='member',
            name='matches',
            field=models.ManyToManyField(related_name='_member_matches_+', to='matchingapp.Member'),
        ),
    ]
