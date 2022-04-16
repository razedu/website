# Generated by Django 4.0.3 on 2022-04-12 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0008_follow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='follows',
        ),
        migrations.RemoveField(
            model_name='follow',
            name='user',
        ),
        migrations.AddField(
            model_name='follow',
            name='following_user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='friends.user', verbose_name='Подписчики'),
        ),
        migrations.AddField(
            model_name='follow',
            name='time_following',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата подписки'),
        ),
        migrations.AddField(
            model_name='follow',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='following', to='friends.user', verbose_name='Пользователь'),
        ),
    ]
