# Generated by Django 2.1.7 on 2019-05-20 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apiv1', '0003_auto_20190518_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buy_request', to='users.Profile'),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(choices=[('sold', 'sold'), ('waiting', 'waiting'), ('declined', 'declined')], default='waiting', max_length=20),
        ),
    ]
