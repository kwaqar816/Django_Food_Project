# Generated by Django 3.2.3 on 2021-06-02 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Foodapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='image',
            field=models.ImageField(default='', upload_to='media'),
        ),
    ]