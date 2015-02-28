# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='the_answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('date', models.DateTimeField(verbose_name=b'answer date')),
                ('rating', models.IntegerField(default=0)),
                ('is_marked_as_true', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='the_question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('text', models.TextField()),
                ('date', models.DateTimeField(verbose_name=b'question date')),
                ('rating', models.IntegerField(default=0)),
                ('the_answer_was_chosen', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='the_tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('used_times', models.IntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='the_user',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=100)),
                ('nickname', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('avatar_link', models.CharField(max_length=200)),
                ('date', models.DateTimeField(verbose_name=b'user was registered')),
                ('rating', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='the_question',
            name='author',
            field=models.ForeignKey(to='core.the_user'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='the_question',
            name='tags',
            field=models.ForeignKey(to='core.the_tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='the_answer',
            name='author',
            field=models.ForeignKey(to='core.the_user'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='the_answer',
            name='contributed_to',
            field=models.ForeignKey(to='core.the_question'),
            preserve_default=True,
        ),
    ]
