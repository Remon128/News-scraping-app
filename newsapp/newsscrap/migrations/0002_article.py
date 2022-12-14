# Generated by Django 3.0.14 on 2022-05-29 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newsscrap', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('articleTitle', models.CharField(max_length=1000)),
                ('articleDesc', models.CharField(max_length=20000)),
                ('articleDOM', models.TextField(max_length=50000)),
                ('articleLink', models.URLField(max_length=8000)),
                ('websiteID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsscrap.Website')),
            ],
        ),
    ]
