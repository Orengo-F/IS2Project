# Generated by Django 2.2.1 on 2022-10-31 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_likepost'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowersCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=100)),
            ],
        ),
    ]
