# Generated by Django 4.2.7 on 2023-11-08 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria_nombre', models.CharField(max_length=50, unique=True)),
                ('descripcion', models.CharField(blank=True, max_length=200, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('categoria_imagen', models.ImageField(blank=True, null=True, upload_to='fotos/categoria')),
            ],
        ),
    ]
