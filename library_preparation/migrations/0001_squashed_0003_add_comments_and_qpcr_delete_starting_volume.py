# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-17 17:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('library_preparation', '0001_initial'), ('library_preparation', '0002_add_timestamps'), ('library_preparation', '0003_add_comments_and_qpcr_delete_starting_volume')]

    initial = True

    dependencies = [
        ('sample', '0003_add_timestamps'),

        # TODO: Uncomment after deleting squashed migrations
        # ('sample', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryPreparation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starting_amount', models.FloatField(blank=True, null=True, verbose_name='Starting Amount')),
                ('spike_in_description', models.TextField(blank=True, null=True, verbose_name='Spike-in Description')),
                ('spike_in_volume', models.FloatField(blank=True, null=True, verbose_name='Spike-in Volume')),
                ('pcr_cycles', models.IntegerField(blank=True, null=True, verbose_name='PCR Cycles')),
                ('concentration_library', models.FloatField(blank=True, null=True, verbose_name='Concentration Library')),
                ('mean_fragment_size', models.IntegerField(blank=True, null=True, verbose_name='Mean Fragment Size')),
                ('nM', models.FloatField(blank=True, null=True, verbose_name='nM')),
                ('sample', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sample.Sample', verbose_name='Sample')),
                ('create_time', models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Create Time')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='Update Time')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='Comments')),
                ('qpcr_result', models.FloatField(blank=True, null=True, verbose_name='qPCR Result')),
            ],
            options={
                'verbose_name': 'Library Preparation',
                'verbose_name_plural': 'Library Preparation',
            },
        ),
    ]
