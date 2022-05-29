# Generated by Django 4.0.4 on 2022-05-29 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_delete_option'),
    ]

    operations = [
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
