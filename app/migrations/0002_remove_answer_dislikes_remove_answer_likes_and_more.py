# Generated by Django 4.0.4 on 2022-05-25 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='views',
        ),
        migrations.RemoveField(
            model_name='question',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='question',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='question',
            name='views',
        ),
        migrations.CreateModel(
            name='LikeQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.profile')),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='question_like', to='app.question')),
            ],
        ),
        migrations.CreateModel(
            name='LikeAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='answer_like', to='app.answer')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.profile')),
            ],
        ),
        migrations.CreateModel(
            name='DisLikeQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.profile')),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='question_dislike', to='app.question')),
            ],
        ),
        migrations.CreateModel(
            name='DisLikeAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='answer_dislike', to='app.answer')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.profile')),
            ],
        ),
    ]