# Generated by Django 3.2.10 on 2021-12-12 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='completed_date',
        ),
        migrations.RemoveField(
            model_name='todo',
            name='hashtags',
        ),
        migrations.AddField(
            model_name='todo',
            name='completed_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='todo',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='HashTag',
        ),
    ]
