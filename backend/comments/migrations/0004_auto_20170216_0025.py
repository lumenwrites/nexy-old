# Generated by Django 2.0.dev20170211211108 on 2017-02-16 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_comment_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]