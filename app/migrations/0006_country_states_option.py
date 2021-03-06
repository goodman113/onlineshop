# Generated by Django 4.0.4 on 2022-05-29 06:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_order_details_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=199, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='States',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=199, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('countries', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.country')),
                ('states', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.states')),
            ],
        ),
    ]
