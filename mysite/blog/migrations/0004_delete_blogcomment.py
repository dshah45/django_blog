# Generated by Django 3.1.3 on 2020-11-26 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogcomment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BlogComment',
        ),
    ]
