# Generated by Django 3.1.5 on 2021-02-16 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('chat', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='chat', to='chat.chats')),
            ],
        ),
        migrations.CreateModel(
            name='ChatUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(default=12)),
                ('chatik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatik', to='chat.chats')),
            ],
        ),
    ]
