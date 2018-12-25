# Generated by Django 2.1.3 on 2018-12-18 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20181217_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likes',
            name='coment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='blog.Coment'),
        ),
        migrations.AlterField(
            model_name='likes',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='blog.Post'),
        ),
    ]
