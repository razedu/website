# Generated by Django 4.0.3 on 2022-05-29 10:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('friends', '0003_remove_profile_id_alter_profile_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'verbose_name': 'Followers', 'verbose_name_plural': 'Followers'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'User post', 'verbose_name_plural': 'User posts'},
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_like', models.DateTimeField(auto_now_add=True, verbose_name='liked_time')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='friends.post', verbose_name='liked_post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL, verbose_name='user_likes')),
            ],
            options={
                'verbose_name': 'Like',
            },
        ),
        migrations.AddConstraint(
            model_name='like',
            constraint=models.UniqueConstraint(fields=('user', 'post'), name='like_unique'),
        ),
    ]
