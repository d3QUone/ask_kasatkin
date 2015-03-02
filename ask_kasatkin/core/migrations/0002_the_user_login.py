# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='the_user',
            name='login',
            field=models.CharField(default=datetime.datetime(2015, 3, 2, 14, 55, 20, 907558, tzinfo=utc), max_length=100),
            preserve_default=False,
        ),
    ]
