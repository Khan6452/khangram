# Generated by Django 2.0.7 on 2018-07-25 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_auto_20180725_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('female', 'Female'), ('male', 'Male'), ('not-specified', 'Not specified')], max_length=80, null=True),
        ),
    ]
