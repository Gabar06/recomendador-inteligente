# Generated by Django 4.2.2 on 2023-06-17 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=60)),
                ('login', models.CharField(max_length=60)),
                ('clave', models.CharField(max_length=60)),
            ],
        ),
    ]
