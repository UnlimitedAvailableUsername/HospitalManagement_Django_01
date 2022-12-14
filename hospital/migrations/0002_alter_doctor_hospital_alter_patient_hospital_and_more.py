# Generated by Django 4.1.2 on 2022-11-11 04:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='hospital',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='hospital.hospitaluser'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='hospital',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='hospital.hospitaluser'),
        ),
        migrations.AlterField(
            model_name='user',
            name='hospital',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='hospital.hospitaluser'),
        ),
    ]
