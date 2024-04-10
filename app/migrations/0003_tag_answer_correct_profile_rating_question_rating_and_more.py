# Generated by Django 5.0.3 on 2024-04-10 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_profile_avatar_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='rating',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='rating',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(blank=True, to='app.tag'),
        ),
    ]
