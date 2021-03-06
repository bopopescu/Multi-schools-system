# Generated by Django 2.2.4 on 2019-12-09 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0020_auto_20191209_1535'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoice',
            options={'default_permissions': ('view', 'add', 'change', 'delete')},
        ),
        migrations.RemoveField(
            model_name='student',
            name='is_absent',
        ),
        migrations.RemoveField(
            model_name='student',
            name='is_late',
        ),
        migrations.RemoveField(
            model_name='student',
            name='is_present',
        ),
        migrations.AddField(
            model_name='student',
            name='absent',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student',
            name='late',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student',
            name='present',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='student',
            name='classroom',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='schools.Classroom'),
        ),
        migrations.AlterField(
            model_name='student',
            name='father_photo',
            field=models.ImageField(blank=True, null=True, upload_to='avatar/'),
        ),
        migrations.AlterField(
            model_name='student',
            name='group',
            field=models.CharField(blank=True, choices=[('Science', 'Science'), ('Arts', 'Arts'), ('Commerce', 'Commerce')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='guardian',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='guardians', to='schools.Guardian'),
        ),
        migrations.AlterField(
            model_name='student',
            name='mother_photo',
            field=models.ImageField(blank=True, null=True, upload_to='avatar/'),
        ),
        migrations.AlterField(
            model_name='student',
            name='registration_no',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='relation_With_Guardian',
            field=models.CharField(blank=True, choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Sister', 'Sister'), ('Bother', 'Bother'), ('Uncle', 'Uncle'), ('Maternal Uncle', 'Maternal Uncle'), ('Aunt', 'Aunt'), ('Other Relative', 'Other Relative')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='roles',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.Role'),
        ),
        migrations.AlterField(
            model_name='student',
            name='roll_no',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='schools.Section'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='schools.StudentType'),
        ),
    ]
