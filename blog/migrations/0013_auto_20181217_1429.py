# Generated by Django 2.1.3 on 2018-12-17 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20181214_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='likes',
            name='coment_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Coment'),
        ),
        migrations.AlterField(
            model_name='likes',
            name='post_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Post'),
        ),
    ]
