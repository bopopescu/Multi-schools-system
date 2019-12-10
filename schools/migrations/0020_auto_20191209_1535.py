# Generated by Django 2.2.4 on 2019-12-09 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0019_remove_invoice_school'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='absent',
        ),
        migrations.RemoveField(
            model_name='student',
            name='late',
        ),
        migrations.RemoveField(
            model_name='student',
            name='present',
        ),
        migrations.AddField(
            model_name='student',
            name='is_absent',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='is_late',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='is_present',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='classroom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='schools.Classroom'),
        ),
        migrations.AlterField(
            model_name='student',
            name='father_photo',
            field=models.FileField(blank=True, null=True, upload_to='avatar/'),
        ),
        migrations.AlterField(
            model_name='student',
            name='group',
            field=models.CharField(blank=True, choices=[('Science', 'Science'), ('Arts', 'Arts'), ('O-Level', 'O-Level')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='guardian',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='guardians', to='schools.Guardian'),
        ),
        migrations.AlterField(
            model_name='student',
            name='mother_photo',
            field=models.FileField(blank=True, null=True, upload_to='avatar/'),
        ),
        migrations.AlterField(
            model_name='student',
            name='registration_no',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='relation_With_Guardian',
            field=models.CharField(blank=True, choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Sister', 'Sister'), ('Bother', 'Bother'), ('Uncle', 'Uncle'), ('Maternal Uncle', 'Maternal Uncle'), ('Aunt', 'Aunt'), ('Other Relative', 'Other Relative')], max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='roles',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='schools.Role'),
        ),
        migrations.AlterField(
            model_name='student',
            name='roll_no',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='schools.Section'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='schools.StudentType'),
        ),
    ]