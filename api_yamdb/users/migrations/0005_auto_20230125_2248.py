# Generated by Django 3.2 on 2023-01-25 18:48

import users.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(
                blank=True,
                max_length=1024,
                verbose_name='Биография пользователя',
            ),
        ),
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(
                blank=True, max_length=10, verbose_name='Код доступа'
            ),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(
                choices=[
                    ('admin', 'admin'),
                    ('moderator', 'moderator'),
                    ('user', 'user'),
                ],
                default='user',
                max_length=1024,
                verbose_name='Роль пользователя',
            ),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(
                max_length=100,
                unique=True,
                validators=[users.validators.validate_username],
                verbose_name='Имя пользователя',
            ),
        ),
    ]
