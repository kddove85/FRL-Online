# Generated by Django 4.0.4 on 2022-05-02 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weekday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=10)),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='scheduleditem',
            name='day_of_the_week',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
