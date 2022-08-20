# Generated by Django 3.0.14 on 2022-05-29 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsscrap', '0004_remove_article_websiteid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='articleDOM',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='article',
            name='articleDesc',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='article',
            name='articleLink',
            field=models.URLField(max_length=1000),
        ),
    ]