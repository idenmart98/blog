# Generated by Django 2.1.3 on 2018-12-17 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20181217_1429'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coment',
            old_name='author_id',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='coment',
            old_name='post_id',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='likes',
            old_name='coment_id',
            new_name='coment',
        ),
        migrations.RenameField(
            model_name='likes',
            old_name='post_id',
            new_name='post',
        ),
    ]
