import uuid
import datetime
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext as _
from taggit.managers import TaggableManager
from tenant_schemas.models import TenantMixin

from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

A = "A"
B = "B"
C = "C"
D = "D"
E = "E"
O = "O"
F = "F"
PASS = "PASS"
FAIL = "FAIL"

GRADE = (
    (A, 'A'),
    (B, 'B'),
    (C, 'C'),
    (D, 'D'),
    (E, 'E'),
    (O, 'O'),
    (F, 'F'),
)

COMMENT = (
    (PASS, "PASS"),
    (FAIL, "FAIL"),
)

BLOOD = (('A+', 'A+'),
         ('A-', 'A-'),
         ('B+', 'B+'),
         ('B-', 'B-'),
         ('O+', 'O+'),
         ('O-', 'O-'),
         ('AB+', 'AB+'),
         ('AB-', 'AB-'))

IS = (('Yes', 'Yes'),
      ('No', 'No'))

ATTENDANCE = (
    ('Present', 'Present'),
    ('Late', 'Late'),
    ('Absent', 'Absent'),
)

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'))

RELIGIONS = (('Christian', 'Christian'),
             ('Muslim', 'Muslim'),
             ('Others', 'Others'))

FIRST = "First"
SECOND = "Second"
THIRD = "Third"

TERM = (
    (FIRST, "First"),
    (SECOND, "Second"),
    (THIRD, "Third"),
)

OPTIONS = (('Yes', 'Yes'),
           ('No', 'No'))

TYPES = (('Incoming', 'Incoming'),
         ('Outgoing', 'Outgoing'))

STATUS = (('Waiting', 'Waiting'),
          ('New', 'New'),
          ('Declined', 'Declined'),
          ('Approved', 'Approved'))

PROTOCOL = (('Mail', 'Mail'),
            ('Sendmail', 'Sendmail'),
            ('smtp', 'smtp'))

PRIORITY = (('Highest', 'Highest'),
            ('Normal', 'Normal'),
            ('Lowest', 'Lowest'))

EMAIL = (('Text', 'Text'),
         ('Html', 'Html'))

SET = (('utf-8', 'utf-8'),
       ('iso-8859-1', 'iso-8859-1'))

Superuser = "Superuser"
Student = "Student"
Guardian = "Guardian"
Teacher = "Teacher"
Admin = "Admin"
Receptionist = "Receptionist"
Librarian = "Librarian"
Accountant = "Accountant"
Staff = "Staff"
Servant = "Servant"
ROLE_CHOICES = (
    (Superuser, 'Superuser'),
    (Student, 'Student'),
    (Teacher, 'Teacher'),
    (Guardian, 'Guardian'),
    (Admin, 'Admin'),
    (Receptionist, 'Receptionist'),
    (Librarian, 'Librarian'),
    (Accountant, 'Accountant'),
    (Staff, 'Staff'),
    (Servant, 'Servant'),
)

MONDAY = 1
TUESDAY = 2
WEDNESDAY = 3
THURSDAY = 4
FRIDAY = 5
SATURDAY = 6
SUNDAY = 7
DAYS_OF_THE_WEEK = (
    (MONDAY, 'Monday'),
    (TUESDAY, 'Tuesday'),
    (WEDNESDAY, 'Wednesday'),
    (THURSDAY, 'Thursday'),
    (FRIDAY, 'Friday'),
    (SATURDAY, 'Saturday'),
    (SUNDAY, 'Sunday'),
)


def GenTimeList():
    StartTime_str = '0100-01-01 08:00:00'
    StartTime = datetime.strptime(StartTime_str, '%Y-%m-%d %H:%M:%S')

    EndTime_str = '0100-01-01 17:00:00'
    EndTime = datetime.strptime(EndTime_str, '%Y-%m-%d %H:%M:%S')

    TimeStep_int = 30
    TimeStep = timedelta(minutes=TimeStep_int)

    TimeList = list()

    TimeInc = StartTime
    while (TimeInc <= EndTime):
        TimeList.append(datetime.strftime(TimeInc, '%H:%M'))
        TimeInc = TimeInc + TimeStep

    return (TimeList)


TimeList = GenTimeList()


class Settings(models.Model):
    brand_name = models.CharField(max_length=130)
    brand_title = models.CharField(max_length=130)
    language = models.CharField(max_length=130)
    enable_RTL = models.CharField(max_length=100, blank=False, choices=IS)
    enable_Frontend = models.CharField(max_length=100, blank=False, choices=IS)
    general_Theme = models.CharField(max_length=130)
    default_time_zone = models.CharField(max_length=130)
    date_format = models.DateField(null=True, default=datetime.now)
    brand_logo = models.ImageField(upload_to='logo/', blank=False)
    favicon_icon = models.ImageField(upload_to='icon/', blank=False)
    brand_footer = models.CharField(max_length=130)
    google_Analytics = models.CharField(max_length=130)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'

    def __str__(self):
        return self.brand_name


# class Holder(TenantMixin):
#     name = models.CharField(max_length=100)
#     description = models.CharField(max_length=100)
#     created_on = models.DateField(auto_now_add=True)
#
#     # default true, schema will be automatically created and synced when it is saved
#     auto_create_schema = True


class School(models.Model):
    school_code = models.CharField(max_length=130, blank=True, null=True)
    school_name = models.CharField(max_length=130)
    address = models.CharField(max_length=130)
    phone = models.CharField(max_length=130)
    registration_date = models.DateField(blank=True, null=True)
    email_address = models.EmailField(max_length=120)
    fax = models.CharField(max_length=130, blank=True, null=True)
    footer = models.CharField(max_length=130, blank=True, null=True)

    currency = models.CharField(max_length=130, blank=True, null=True)
    currency_symbol = models.CharField(max_length=130)

    enable_frontend = models.CharField(max_length=130, blank=False, choices=OPTIONS)
    RESULTS = (('Average of all exams', 'Average of all exams'),
               ('Only based on final exams', 'Only based on final exams'))
    exam_final_result = models.CharField(max_length=130, blank=False, choices=RESULTS)
    latitude = models.CharField(max_length=130, blank=True, null=True)
    longitude = models.CharField(max_length=130, blank=True, null=True)
    api_key = models.CharField(max_length=130, blank=True, null=True)
    online_Admission = models.CharField(max_length=130, blank=False, choices=OPTIONS)

    facebook_url = models.URLField(max_length=130, blank=True, null=True)
    twitter_url = models.URLField(max_length=130, blank=True, null=True)
    linkedIn_url = models.URLField(max_length=130, blank=True, null=True)
    google_plus_url = models.URLField(max_length=130, blank=True, null=True)
    youtube_url = models.URLField(max_length=130, blank=True, null=True)
    instagram_url = models.URLField(max_length=130, blank=True, null=True)
    pinterest_url = models.URLField(max_length=130, blank=True, null=True)

    frontend_Logo = models.ImageField(upload_to='logo/', blank=False)
    backend_Logo = models.ImageField(upload_to='logo/', blank=False)

    STATUS = (('Active', 'Active'),
              ('Inactive', 'Inactive'))
    status = models.CharField(max_length=130, blank=True, null=True, default="Active", choices=STATUS)
    THEMES = (('Black', 'Black'),
              ('Navy Blue', 'Navy Blue'),
              ('Red', 'Red'),
              ('Maroon', 'Maroon'),
              )
    theme = models.CharField(max_length=130, choices=THEMES)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        ordering = ('school_name',)
        verbose_name = 'school'
        verbose_name_plural = 'schools'

    def __str__(self):
        return self.school_name


class UserManager(BaseUserManager):
    def Create_user(self, username, password=None):
        if not username:
            raise ValueError("Users must have a user name")

        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.Create_user(
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    username = models.CharField(max_length=30, unique=True)
    national_ID = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100)

    gender = models.CharField(max_length=100, blank=True, choices=GENDER)
    religion = models.CharField(max_length=100, blank=True, null=True, choices=RELIGIONS)

    present_address = models.CharField(max_length=100, blank=True, null=True)
    permanent_address = models.CharField(max_length=100, blank=True, null=True)
    blood_group = models.CharField(max_length=100, blank=True, null=True, choices=BLOOD)
    birth_date = models.DateField(null=True, blank=True)
    other_info = models.TextField(max_length=200)
    photo = models.ImageField(upload_to='avatars/', blank=False)
    is_active = models.BooleanField(default=True)  # can login
    is_staff = models.BooleanField(default=False)  # staff user non superuser
    joining_date = models.DateField(verbose_name="date joined", null=True, auto_now=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)

    is_superuser = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_guardian = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    roles = models.ForeignKey('Role', on_delete=models.CASCADE, blank=True, null=True)

    USERNAME_FIELD = 'username'  # username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = []  # ['full_name'] #python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        if self.full_name:
            return self.full_name
        return self.username

    def get_picture(self):
        no_picture = settings.STATIC_URL + 'img/img_avatar.png'
        try:
            return self.photo.url
        except:
            return no_picture

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Role(models.Model):
    role_name = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    note = models.CharField(max_length=130)
    is_default = models.CharField(max_length=100, blank=True, choices=OPTIONS)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.role_name


class EmailSetting(models.Model):
    email_protocol = models.CharField(max_length=100, blank=True, choices=PROTOCOL)
    email_type = models.CharField(max_length=100, blank=True, choices=EMAIL)
    char_set = models.CharField(max_length=100, blank=True, choices=SET)
    priority = models.CharField(max_length=100, blank=True, choices=PRIORITY)
    email_from_name = models.CharField(max_length=300)
    email_from_address = models.CharField(max_length=300)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.email_protocol


class Designation(models.Model):
    designation = models.CharField(max_length=130)
    note = models.TextField(max_length=300)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.designation


class Feedback(models.Model):
    feedback = models.TextField(max_length=300)
    is_publish = models.CharField(max_length=130, blank=False, choices=OPTIONS)
    date = models.DateField(null=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.feedback


class Superuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='superuser')
    roles = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False, null=True)
    resume = models.ImageField(upload_to='resume/', blank=False)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.user.full_name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    responsibility = models.CharField(max_length=200)
    roles = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False, null=True)
    resume = models.FileField(upload_to='resume/', blank=False)
    salary_grade = models.ForeignKey('SalaryGrade', on_delete=models.CASCADE, blank=False, null=True)
    TYPE = (('Monthly', 'Monthly'),
            ('Hourly', 'Hourly'))
    salary_type = models.CharField(max_length=100, choices=TYPE)
    facebook_url = models.URLField(max_length=130, blank=True, null=True)
    twitter_url = models.URLField(max_length=130, blank=True, null=True)
    linkedIn_url = models.URLField(max_length=130, blank=True, null=True)
    google_plus_url = models.URLField(max_length=130, blank=True, null=True)
    youtube_url = models.URLField(max_length=130, blank=True, null=True)
    instagram_url = models.URLField(max_length=130, blank=True, null=True)
    pinterest_url = models.URLField(max_length=130, blank=True, null=True)
    IS = (('Yes', 'Yes'),
          ('No', 'No'))
    Is_View_on_Web = models.CharField(max_length=100, blank=False, choices=IS)

    present = models.IntegerField(default=0)
    absent = models.IntegerField(default=0)
    late = models.IntegerField(default=0)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.user.full_name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')

    designation = models.ForeignKey('Designation', on_delete=models.CASCADE, blank=False, null=True)
    salary_grade = models.ForeignKey('SalaryGrade', on_delete=models.CASCADE, blank=False, null=True)
    TYPE = (('Monthly', 'Monthly'),
            ('Hourly', 'Hourly'))
    salary_type = models.CharField(max_length=100, blank=False, choices=TYPE)
    roles = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False, null=True)
    resume = models.FileField(upload_to='resume/', blank=False)
    facebook_url = models.URLField(max_length=130, blank=True, null=True)
    twitter_url = models.URLField(max_length=130, blank=True, null=True)
    linkedIn_url = models.URLField(max_length=130, blank=True, null=True)
    google_plus_url = models.URLField(max_length=130, blank=True, null=True)
    youtube_url = models.URLField(max_length=130, blank=True, null=True)
    instagram_url = models.URLField(max_length=130, blank=True, null=True)
    pinterest_url = models.URLField(max_length=130, blank=True, null=True)
    Is_View_on_Web = models.CharField(max_length=100, blank=False, choices=IS)
    joining_date = models.DateField(null=True, blank=True)

    present = models.IntegerField(default=0)
    absent = models.IntegerField(default=0)
    late = models.IntegerField(default=0)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.user.full_name


class Guardian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guardian')
    roles = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False, null=True)
    profession = models.CharField(max_length=100)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.user.full_name


class Discounting(models.Model):
    title = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)
    note = models.TextField(max_length=300)

    def __str__(self):
        return self.title

    @property
    def discountamount(self):
        return self.amount


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    admission_no = models.CharField(max_length=100, unique=True)
    admission_date = models.DateField(null=True)
    guardian = models.ForeignKey('Guardian', on_delete=models.CASCADE, blank=False, null=True, related_name='guardians')
    RELATION = (('Father', 'Father'),
                ('Mother', 'Mother'),
                ('Sister', 'Sister'),
                ('Bother', 'Bother'),
                ('Uncle', 'Uncle'),
                ('Maternal Uncle', 'Maternal Uncle'),
                ('Aunt', 'Aunt'),
                ('Other Relative', 'Other Relative'))
    relation_With_Guardian = models.CharField(max_length=100, blank=True, null=True, choices=RELATION)
    classroom = models.ForeignKey('Classroom', on_delete=models.SET_NULL, blank=False, null=True)
    section = models.ForeignKey('Section', on_delete=models.SET_NULL, blank=False, null=True)
    student_type = models.ForeignKey('StudentType', on_delete=models.SET_NULL, blank=False, null=True)
    GROUP = (
        ('Science', 'Science'),
        ('Arts', 'Arts'),
        ('Commerce', 'Commerce'))
    group = models.CharField(max_length=100, blank=True, null=True, choices=GROUP)
    roll_no = models.CharField(max_length=100, unique=True)
    registration_no = models.CharField(max_length=100, blank=True, null=True)
    roles = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False, null=True)
    fees_discount =models.ForeignKey(Discounting, on_delete=models.CASCADE, blank=True, null=True)
    second_language = models.CharField(max_length=100, blank=True, null=True)
    caste = models.CharField(max_length=100, blank=True, null=True)

    previous_school = models.CharField(max_length=100, blank=True, null=True)
    previous_class = models.CharField(max_length=100, blank=True, null=True)
    transfer_certificate = models.FileField(upload_to='certificates/', null=True, blank=True)

    father_name = models.CharField(max_length=100, blank=True, null=True)
    father_phone = models.CharField(max_length=100, blank=True, null=True)
    father_education = models.CharField(max_length=100, blank=True, null=True)
    father_profession = models.CharField(max_length=100, blank=True, null=True)
    father_designation = models.CharField(max_length=100, blank=True, null=True)
    father_photo = models.ImageField(upload_to='avatar/', null=True, blank=True)

    mother_name = models.CharField(max_length=100, blank=True, null=True)
    mother_phone = models.CharField(max_length=100, blank=True, null=True)
    mother_education = models.CharField(max_length=100, blank=True, null=True)
    mother_profession = models.CharField(max_length=100, blank=True, null=True)
    mother_designation = models.CharField(max_length=100, blank=True, null=True)
    mother_photo = models.ImageField(upload_to='avatar/', null=True, blank=True)
    health_condition = models.CharField(max_length=100, blank=True, null=True)

    present = models.IntegerField(default=0)
    absent = models.IntegerField(default=0)
    late = models.IntegerField(default=0)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    @property
    def feesdiscount(self):
        return self.fees_discount.discountamount

    def __str__(self):
        return self.user.full_name


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if instance.is_superuser:
        Superuser.objects.get_or_create(user=instance)

    if instance.is_teacher:
        Teacher.objects.get_or_create(user=instance)

    if instance.is_student:
        Student.objects.get_or_create(user=instance)

    if instance.is_guardian:
        Guardian.objects.get_or_create(user=instance)

    if instance.is_employee:
        Employee.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user(sender, instance, **kwargs):
    if instance.is_superuser:
        instance.superuser.save()

    if instance.is_teacher:
        instance.teacher.save()

    if instance.is_student:
        instance.student.save()

    if instance.is_employee:
        instance.employee.save()

    if instance.is_guardian:
        instance.guardian.save()


class StudentPaidFees(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, blank=True, null=True)
    paid_amount = models.IntegerField(default=0)
    method = (('Cash', 'Cash'), ('Cheque', 'Cheque'))
    methods = (('Unpaid', 'Unpaid'), ('Partial', 'Partial'), ('Paid', 'Paid'))
    paid_status = models.CharField(max_length=100, choices=methods, blank=True, null=True)
    Payment_Method = models.CharField(max_length=100, choices=method, blank=True, null=True)
    Bank_Name = models.CharField(max_length=100, blank=True, null=True)
    Cheque_Number = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(max_length=100)

    def __str__(self):
        return self.paid_amount


class StudentType(models.Model):
    student_type = models.CharField(max_length=100, blank=True)
    note = models.TextField(max_length=130)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.student_type


class Activity(models.Model):
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE, blank=False, null=True)
    section = models.ForeignKey('Section', on_delete=models.CASCADE, blank=False, null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    activity_date = models.DateField(blank=True, null=True)
    activity = models.TextField(max_length=130)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.activity


class Card(models.Model):
    border_color = models.CharField(max_length=130)
    top_background = models.CharField(max_length=130)
    card_school_name = models.CharField(max_length=130)
    school_name_font_size = models.CharField(max_length=130)
    school_name_color = models.CharField(max_length=130)
    school_address = models.CharField(max_length=130)
    school_address_color = models.CharField(max_length=130)
    admit_card_font_size = models.CharField(max_length=130)
    admit_card_color = models.CharField(max_length=130)
    admit_card_background = models.CharField(max_length=130)
    title_font_size = models.CharField(max_length=130)
    title_color = models.CharField(max_length=130)
    value_font_size = models.CharField(max_length=130)
    value_color = models.CharField(max_length=130)
    exam_font_size = models.CharField(max_length=130)
    exam_color = models.CharField(max_length=130)
    subject_font_size = models.CharField(max_length=130)
    subject_color = models.CharField(max_length=130)
    bottom_signature = models.CharField(max_length=130)
    signature_background = models.CharField(max_length=130)
    signature_color = models.CharField(max_length=130)
    signature_align = models.CharField(max_length=130)
    admit_card_logo = models.ImageField(upload_to='card/', null=True, blank=False)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.card_school_name


class Classroom(models.Model):
    classroom = models.CharField(max_length=130)
    numeric_name = models.CharField(max_length=130)
    class_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=False, null=True)
    note = models.CharField(max_length=130)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        ordering = ('classroom',)
        verbose_name = 'classroom',
        verbose_name_plural = 'classrooms'

    def __str__(self):
        return self.classroom


class Section(models.Model):
    section = models.CharField(max_length=130)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    section_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=False, null=True)
    note = models.CharField(max_length=130)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        ordering = ('section',)
        verbose_name = 'section'
        verbose_name_plural = 'sections'

    def __str__(self):
        return self.section


class Year(models.Model):
    year = models.CharField(max_length=200, unique=True)
    is_current_year = models.BooleanField(default=False, blank=True, null=True)
    note = models.TextField(max_length=300)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.year


class Term(models.Model):
    term = models.CharField(max_length=10, choices=TERM, blank=True)
    is_current_term = models.BooleanField(default=False, blank=True, null=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, blank=True, null=True)
    next_term_begins = models.DateField(null=True, blank=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.term


class Subject(models.Model):
    subject_name = models.CharField(max_length=130)
    subject_code = models.CharField(max_length=130)
    subject_unit = models.CharField(max_length=200)
    description = models.TextField(max_length=200, blank=True)
    subject_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=False, null=True)

    TYPE = (('Mandatory', 'Mandatory'),
            ('Optional', 'Optional'))
    type = models.CharField(max_length=100, blank=False, choices=TYPE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    term = models.CharField(choices=TERM, max_length=200)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, blank=True, null=True)
    note = models.TextField(max_length=250)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.subject_name

    def get_absolute_url(self):
        return reverse('subject_list', kwargs={'pk': self.pk})

    def get_total_subjects(self):
        t = 0
        total = Subject.objects.all()
        for i in total:
            t += i
        return t


class TakenSubject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='taken_subjects', blank=False,
                                null=True)
    bot = models.PositiveIntegerField(blank=True, null=True, default=0)
    mot = models.PositiveIntegerField(blank=True, null=True, default=0)
    eot = models.PositiveIntegerField(blank=True, null=True, default=0)
    total = models.PositiveIntegerField(blank=True, null=True, default=0)
    grade = models.CharField(choices=GRADE, max_length=1, blank=True)
    comment = models.CharField(choices=COMMENT, max_length=200, blank=True)

    def __str__(self):
        return '{} - {} {} - {}'.format(self.id, self.student, self.subject, self.grade)

    def get_absolute_url(self):
        return reverse('update_score', kwargs={'pk': self.pk})

    def get_total(self, bot, mot, eot):
        return int(bot) + int(mot) + int(eot)

    def get_grade(self, bot, mot, eot):
        total = int(bot) + int(mot) + int(eot)
        if total >= 80:
            grade = A
        elif total >= 70:
            grade = B
        elif total >= 60:
            grade = C
        elif total >= 50:
            grade = D
        elif total >= 40:
            grade = E
        elif total >= 30:
            grade = O
        else:
            grade = F
        return grade

    def get_comment(self, grade):
        if not grade == "F":
            comment = PASS
        else:
            comment = FAIL
        return comment

    def carry_over(self, grade):
        if grade == F:
            CarryOverStudent.objects.get_or_create(student=self.student, subject=self.subject)
        else:
            try:
                CarryOverStudent.objects.get(student=self.student, subject=self.subject).delete()
            except:
                pass

    def is_repeating(self, grade):
        # count = CarryOverStudent.objects.filter(student__id=self.student.id)
        # units = 0
        # for i in count:
        #     units += int(i.subject.subject_unit)
        # if count.count() >= 6 or units >= 16:
        if grade == F:
            RepeatingStudent.objects.get_or_create(student=self.student, classroom=self.student.classroom)
        else:
            try:
                RepeatingStudent.objects.get(student=self.student, classroom=self.student.classroom).delete()
            except:
                pass

    def calculate_gpa(self, total_unit_in_term):
        current_term = Term.objects.get(is_current_term=True)
        student = TakenSubject.objects.filter(student=self.student, subject__classroom=self.student.classroom,
                                              subject__term=current_term)
        p = 0
        point = 0
        for i in student:
            subject_unit = i.subject.subject_unit
            if i.grade == A:
                point = 6
            elif i.grade == B:
                point = 5
            elif i.grade == C:
                point = 4
            elif i.grade == D:
                point = 3
            elif i.grade == E:
                point = 2
            elif i.grade == O:
                point = 1
            else:
                point = 0
            p += int(subject_unit) * point
        try:
            gpa = (p / total_unit_in_term)
            return round(gpa, 1)
        except ZeroDivisionError:
            return 0

    def calculate_cgpa(self):
        current_term = Term.objects.get(is_current_term=True)
        previous_result = Result.objects.filter(student__id=self.student.id, classroom__lt=self.student.classroom)
        previous_CGPA = 0
        for i in previous_result:
            if i.cgpa is not None:
                previous_CGPA += i.cgpa
        cgpa = 0
        if str(current_term) == SECOND:
            try:
                first_term_gpa = Result.objects.get(student=self.student.id, term=FIRST,
                                                    classroom=self.student.classroom)
                first_term_gpa += first_term_gpa.gpa.gpa
            except:
                first_term_gpa = 0

            try:
                sec_term_gpa = Result.objects.get(student=self.student.id, term=SECOND,
                                                  classroom=self.student.classroom)
                sec_term_gpa += sec_term_gpa.gpa
            except:
                sec_term_gpa = 0

            taken_subjects = TakenSubject.objects.filter(student=self.student,
                                                         student__classroom=self.student.classroom)
            TSU = 0
            for i in taken_subjects:
                TSU += int(i.subject.subject_unit)
            cpga = first_term_gpa + sec_term_gpa / TSU

            return round(cgpa, 2)


class CarryOverStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)
    term = models.CharField(max_length=100, choices=TERM, blank=True, null=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.student.admission_no


class RepeatingStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return self.student.admission_no


class Syllabus(models.Model):
    syllabus_title = models.CharField(max_length=130)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, blank=False, null=True)
    syllabus = models.FileField(upload_to='syllabus/', null=True, blank=False)
    note = models.TextField(max_length=250)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        verbose_name = _("Syllabus")
        verbose_name_plural = _("Syllabus")

    def __str__(self):
        return self.syllabus_title


class Material(models.Model):
    material_title = models.CharField(max_length=130)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)
    material = models.FileField(upload_to='material/', null=True, blank=False)
    description = models.TextField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.material_title


class Routine(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=False, null=True)
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)
    day = models.IntegerField(choices=DAYS_OF_THE_WEEK, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=False, null=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    room_no = models.CharField(max_length=130)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        ordering = ('day', 'start_time')
        verbose_name = _('Routine')
        verbose_name_plural = _('Routine')

    def __str__(self):
        return '{} - {} {} - {}'.format(self.id, self.day, self.start_time, self.subject_name)


class BulkStudent(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=False, null=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, default=1)
    date = models.DateField()
    status = models.CharField(max_length=50, choices=ATTENDANCE)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        ordering = ["date", ]
        get_latest_by = "date"


class TeacherAttendance(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=False, null=True)
    date = models.DateField()
    status = models.CharField(max_length=50, choices=ATTENDANCE)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        ordering = ["date", ]
        get_latest_by = "date"


class EmployeeAttendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=False, null=True)
    date = models.DateField()
    status = models.CharField(max_length=50, choices=ATTENDANCE)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        ordering = ["date", ]
        get_latest_by = "date"


class AbsentEmail(models.Model):
    receiver_type = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    absent_user = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    template = models.CharField(max_length=100)
    absent_date = models.DateField(null=True)
    subject = models.CharField(max_length=100)
    email_body = models.TextField(max_length=300)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')


class AbsentSMS(models.Model):
    receiver_type = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    absent_user = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    template = models.CharField(max_length=100)
    absent_date = models.DateField(null=True)
    SMS = models.TextField(max_length=300)
    gateway = models.CharField(max_length=100)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')


class Assignment(models.Model):
    assignment_title = models.CharField(max_length=100)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)
    deadline = models.DateField(null=True)
    assignment = models.FileField(upload_to='assignment/', null=True, blank=False)
    note = models.TextField(max_length=300)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')


class ExamGrade(models.Model):
    exam_grade = models.CharField(max_length=100)
    grade_point = models.CharField(max_length=100)
    mark_from = models.CharField(max_length=100)
    mark_to = models.CharField(max_length=100)
    note = models.TextField(max_length=300)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.exam_grade


class Exam(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=True, null=True)
    exam_title = models.CharField(max_length=100)
    start_date = models.DateField(null=True)
    note = models.TextField(max_length=300)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.exam_title


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False, null=True)
    gpa = models.FloatField(null=True)
    cgpa = models.FloatField(null=True)
    term = models.CharField(max_length=100, choices=TERM)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return '{} - {} {} - {}'.format(self.id, self.student, self.classroom, self.year)


class Mark(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=False, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False, null=True)
    bot = models.PositiveIntegerField(blank=True, null=True, default=0)
    mot = models.PositiveIntegerField(blank=True, null=True, default=0)
    eot = models.PositiveIntegerField(blank=True, null=True, default=0)
    total = models.PositiveIntegerField(blank=True, null=True, default=0)
    grade = models.CharField(choices=GRADE, max_length=1, blank=True)
    comment = models.TextField(max_length=300, default=PASS)

    def get_total(self, bot, mot, eot):
        return int(bot) + int(mot) + int(eot)

    def get_grade(self, bot, mot, eot):
        total = int(bot) + int(mot) + int(eot)
        if total >= 80:
            grade = A
        elif total >= 70:
            grade = B
        elif total >= 60:
            grade = C
        elif total >= 45:
            grade = D
        elif total >= 35:
            grade = E
        else:
            grade = F
        return grade

    def get_comment(self, grade):
        if not grade == "F":
            comment = PASS
        else:
            comment = FAIL
        return comment

    def calculate_aggregate(self, total_exams_in_term):
        current_term = Term.objects.get(is_current_term=False)
        student = Mark.objects.filter(student=self.student, subject__classroom=self.student.classroom)
        p = 0
        point = 0
        for i in student:
            exam = i.exam.exam_title
            if i.grade == A:
                point = 5
            elif i.grade == B:
                point = 4
            elif i.grade == C:
                point = 3
            elif i.grade == D:
                point = 2
            elif i.grade == E:
                point = 1
            else:
                point = 0
            p += int(exam) * point
        try:
            aggregate = (p / total_exams_in_term)
            return round(aggregate, 1)
        except ZeroDivisionError:
            return 0

    def calculate_(self):
        exams = Mark.objects.filter(student=self.student, student__classroom=self.student.classroom)
        total = 0
        for i in exams:
            total += int(i.exam.exam_title)

        return round(total, 2)


class ExamSchedule(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)
    exam_date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    room_no = models.CharField(max_length=300)
    note = models.TextField(max_length=300)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')


class ExamSuggestion(models.Model):
    suggestion_title = models.CharField(max_length=300)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)
    suggestion = models.FileField(upload_to='suggestion/', null=True, blank=False)
    note = models.TextField(max_length=300)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.suggestion_title


class ExamAttendance(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=False, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')


class Promotion(models.Model):
    running_session = models.CharField(max_length=100)
    promote_to_session = models.CharField(max_length=100)
    current_class = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    promote_to_class = models.CharField(max_length=100)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')


class CertificateType(models.Model):
    certificate_name = models.CharField(max_length=100)
    school_name = models.CharField(max_length=100)
    certificate_text = models.TextField(max_length=400)
    footer_left_text = models.CharField(max_length=100)
    footer_middle_text = models.CharField(max_length=100)
    footer_right_text = models.CharField(max_length=100)
    background = models.ImageField(upload_to='background/', null=True, blank=False)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.certificate_name


class GenerateCertificate(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    certificate_type = models.ForeignKey(CertificateType, on_delete=models.CASCADE, blank=False, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')


class Book(models.Model):
    book_title = models.CharField(max_length=100)
    book_ID = models.CharField(max_length=100)
    ISBN_no = models.CharField(max_length=100)
    edition = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    almira_no = models.CharField(max_length=100)
    book_cover = models.ImageField(upload_to='cover', blank=False)
    created = models.DateField(verbose_name="Created", auto_now=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.book_title


class EBook(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=False, null=True)
    EBook_title = models.CharField(max_length=100)
    edition = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='cover', blank=False)
    e_book = models.ImageField(upload_to='ebook', blank=False)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        verbose_name = _("E-Book")
        verbose_name_plural = _("E-Books")

    def __str__(self):
        return self.EBook_title


class LibraryMember(models.Model):
    photo = models.ImageField(upload_to='avatar/', null=True, blank=False)
    library_ID = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    classroom = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=100)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.name


class Issue(models.Model):
    select_book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=False, null=True)
    library_member = models.ForeignKey(LibraryMember, on_delete=models.CASCADE, blank=False, null=True)
    ISBN_no = models.CharField(max_length=100)
    edition = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    almira_no = models.CharField(max_length=100)
    book_cover = models.ImageField(upload_to='cover/', null=True, blank=False)
    issue_date = models.DateField(null=True)
    due_date = models.DateField(null=True)
    return_date = models.DateField(null=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.select_book


class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)
    driver = models.CharField(max_length=100)
    vehicle_licence = models.CharField(max_length=100)
    vehicle_contact = models.CharField(max_length=100)
    note = models.CharField(max_length=100)
    created = models.DateField(verbose_name="Created", auto_now=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.vehicle_number


class Type(models.Model):
    complain_type = models.CharField(max_length=100)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.complain_type


class Complain(models.Model):
    complain_user_type = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False, null=True)
    complain_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    complain_type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=False, null=True)
    complain_date = models.DateField(null=True)
    action_date = models.DateField(null=True)
    complain = models.TextField(max_length=400)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.complain_user


class Route(models.Model):
    route_title = models.CharField(max_length=100)
    route_start = models.CharField(max_length=100)
    route_end = models.CharField(max_length=100)
    vehicle_for_route = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=False, null=True)
    stop_name = models.CharField(max_length=100)
    stop_km = models.CharField(max_length=100)
    stop_fare = models.CharField(max_length=100)
    note = models.CharField(max_length=100)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.route_title


class TransportMember(models.Model):
    photo = models.ImageField(upload_to='avatar/', null=True, blank=False)
    name = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=False, null=True)
    roll_no = models.CharField(max_length=100)
    transport_route_name = models.ForeignKey(Route, on_delete=models.CASCADE, blank=False, null=True)
    stop_Name = models.CharField(max_length=100)
    stop_KM = models.CharField(max_length=100)
    stop_Fare = models.CharField(max_length=100)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.name


class Hostel(models.Model):
    hostel_name = models.CharField(max_length=100)
    TYPE = (
        ('Single - Boys', 'Single - Boys'),
        ('Single - Girls', 'Single - Girls'),
        ('Mixed', 'Mixed'))
    hostel_type = models.CharField(max_length=100, blank=False, choices=TYPE)
    address = models.CharField(max_length=100)
    note = models.TextField(max_length=300)
    created = models.DateField(verbose_name="Created", auto_now=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.hostel_name


class Room(models.Model):
    room_no = models.CharField(max_length=100)
    TYPE = (
        ('AC', 'AC'),
        ('Non AC', 'Non AC'))
    room_type = models.CharField(max_length=100, blank=False, choices=TYPE)
    seat_total = models.CharField(max_length=100)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, blank=False, null=True)
    cost_per_seat = models.CharField(max_length=100)
    note = models.TextField(max_length=300)
    created = models.DateField(verbose_name="Created", auto_now=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.room_no


class HostelMember(models.Model):
    photo = models.ImageField(upload_to='avatar/', null=True, blank=False)
    name = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=False, null=True)
    roll_no = models.CharField(max_length=100)
    hostel_name = models.ForeignKey(Hostel, on_delete=models.CASCADE, blank=False, null=True)
    room_no = models.ForeignKey(Room, on_delete=models.CASCADE, blank=False, null=True)
    TYPE = (
        ('AC', 'AC'),
        ('Non AC', 'Non AC'))
    room_type = models.CharField(max_length=100, blank=False, choices=TYPE)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')


class Email(models.Model):
    receiver_type = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    receiver = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    subject = models.CharField(max_length=100)
    email_body = models.TextField(max_length=300)
    attachment = models.FileField(upload_to='attachment/', null=True, blank=False)
    send_time = models.DateTimeField(verbose_name="Modified", auto_now=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')


class SMS(models.Model):
    receiver_type = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    receiver = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    SMS = models.TextField(max_length=300)
    gateway = models.CharField(max_length=100)
    send_time = models.DateTimeField(verbose_name="Modified", auto_now=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        verbose_name = _("SMS")
        verbose_name_plural = _("SMS")


class MessageQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability."""

    def get_conversation(self, sender, recipient):
        """Returns all the messages sent between two users."""
        qs_one = self.filter(sender=sender, recipient=recipient)
        qs_two = self.filter(sender=recipient, recipient=sender)
        return qs_one.union(qs_two).order_by('timestamp')

    def get_most_recent_conversation(self, recipient):
        """Returns the most recent conversation counterpart's username."""
        try:
            qs_sent = self.filter(sender=recipient)
            qs_recieved = self.filter(recipient=recipient)
            qs = qs_sent.union(qs_recieved)
            # .latest("timestamp")
            # if qs.sender == recipient:
            #     return qs.recipient
            #
            # return qs.sender

        except self.model.DoesNotExist:
            return get_user_model().objects.get(username=recipient.username)

    def mark_conversation_as_read(self, sender, recipient):
        """Mark as read any unread elements in the current conversation."""
        qs = self.filter(sender=sender, recipient=recipient)
        return qs.update(unread=False)


class Message(models.Model):
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    receiver_type = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages',
                               verbose_name=_("Sender"), null=True, on_delete=models.SET_NULL)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', null=True,
                                  blank=True, verbose_name=_("Recipient"), on_delete=models.SET_NULL)
    subject = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    message = models.TextField(max_length=300, blank=True)
    timestamp = models.DateTimeField(verbose_name="Modified", auto_now=True)
    unread = models.BooleanField(default=True, db_index=True)
    objects = MessageQuerySet.as_manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ("-timestamp",)

    def __str__(self):
        return self.message

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    @staticmethod
    def send_message(sender, recipient, message):
        new_message = Message.objects.create(
            sender=sender,
            recipient=recipient,
            message=message
        )
        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive',
            'key': 'message',
            'message_id': new_message.uuid_id,
            'sender': sender,
            'recipient': recipient
        }
        async_to_sync(channel_layer.group_send)(recipient.username, payload)
        return new_message


class Notice(models.Model):
    notice_title = models.CharField(max_length=100)
    date = models.DateField(null=True)
    notice_for = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    notice = models.TextField(max_length=300)
    IS = (('Yes', 'Yes'),
          ('No', 'No'))
    Is_View_on_Web = models.CharField(max_length=100, blank=False, choices=IS)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')


class News(models.Model):
    news_title = models.CharField(max_length=100)
    date = models.DateField(null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=False)
    news = models.TextField(max_length=300)
    IS = (('Yes', 'Yes'),
          ('No', 'No'))
    Is_View_on_Web = models.CharField(max_length=100, blank=False, choices=IS)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        verbose_name = _("News")
        verbose_name_plural = _("News")


class Holiday(models.Model):
    holiday_title = models.CharField(max_length=100)
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    note = models.TextField(max_length=300)
    IS = (('Yes', 'Yes'),
          ('No', 'No'))
    Is_View_on_Web = models.CharField(max_length=100, blank=False, choices=IS)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')


class Event(models.Model):
    event_title = models.CharField(max_length=100)
    event_for = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    event_place = models.CharField(max_length=100)
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=False)
    note = models.TextField(max_length=300)
    IS = (('Yes', 'Yes'),
          ('No', 'No'))
    Is_View_on_Web = models.CharField(max_length=100, blank=False, choices=IS)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')


class SalaryGrade(models.Model):
    academic_year = models.ForeignKey(Year, on_delete=models.CASCADE, blank=True, null=True)
    payee = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=True, null=True)
    grade_name = models.CharField(max_length=100)
    basic_salary = models.CharField(max_length=100)
    house_rent = models.CharField(max_length=100)
    transport_allowance = models.CharField(max_length=100)
    medical_allowance = models.CharField(max_length=100)
    over_time_hourly_pay = models.CharField(max_length=100)
    provident_fund = models.CharField(max_length=100)
    hourly_rate = models.CharField(max_length=100)
    total_allowance = models.CharField(max_length=100, blank=True, null=True)
    total_deduction = models.CharField(max_length=100, blank=True, null=True)
    gross_salary = models.CharField(max_length=100, blank=True, null=True)
    net_salary = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(null=True, blank=False)
    over_time_total_hour = models.CharField(max_length=100, blank=True, null=True)
    over_time_amount = models.CharField(max_length=100, blank=True, null=True)
    Bonus = models.CharField(max_length=100, blank=True, null=True)
    Penalty = models.CharField(max_length=100, blank=True, null=True)
    Month = models.CharField(max_length=100, blank=True, null=True)
    pay = (('Cheque', 'Cheque'),
           ('MobileMoney', 'MobileMoney'),
           ('Cash', 'Cash'))
    Payment_Method = models.CharField(max_length=100, choices=pay, blank=True, null=True)
    Bank_Name = models.CharField(max_length=100, blank=True, null=True)
    Cheque_Number = models.CharField(max_length=100, blank=True, null=True)
    Expenditure_Head = models.ForeignKey('ExpenditureHead', on_delete=models.CASCADE, blank=True, null=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.grade_name


class FeeType(models.Model):
    IS = (('GeneralFee', 'GeneralFee'),
          ('Hostel', 'Hostel'),
          ('Transport', 'Transport'))
    fee_type = models.CharField(max_length=100, blank=False, choices=IS)
    Class_Amount = models.IntegerField(blank=True, null=True, default=0)
    Class = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=True, null=True)
    fee_title = models.CharField(max_length=100)
    note = models.TextField(max_length=300)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.fee_title

    @property
    def classamount(self):
        return self.Class_Amount


class PaidDues(models.Model):
    student_id = models.CharField(max_length=100, blank=True, null=True)
    classroom = models.CharField(max_length=100, blank=True, null=True)
    student_name = models.CharField(max_length=100, blank=True, null=True)
    paid_amount = models.IntegerField(default=0)
    Payment_Method = models.CharField(max_length=100, blank=True, null=True)
    Bank_Name = models.CharField(max_length=100, blank=True, null=True)
    Cheque_Number = models.CharField(max_length=100, blank=True, null=True)
    note = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    '''@property
    def deleting(self):
        if(paid_status > 0):
            self.delete()'''


class Invoice(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True, related_name='use')
    discount = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True, related_name='fee_discount')
    fee_type = models.ForeignKey(FeeType, on_delete=models.CASCADE, blank=True, null=True, related_name='fee')
    fee_amount = models.ForeignKey(FeeType, on_delete=models.CASCADE, blank=True, null=True, related_name='fee_am')
    paid_amount = models.IntegerField(default=0, blank=True, null=True)
    month = models.DateField(max_length=100, blank=True, null=True)
    paid = 'PAID'
    partial = 'PARTIAL'
    unpaid = 'UNPAID'
    state = ((paid, 'Paid'), (partial, 'Partial'), (unpaid, 'Unpaid'))
    method = (('Cash', 'Cash'), ('Cheque', 'Cheque'))
    date = models.DateField(auto_now_add=True)
    net_amount = models.IntegerField(default=0, blank=True, null=True)
    paid_status = models.CharField(max_length=100, blank=True, null=True, choices=state, default=unpaid)
    Payment_Method = models.CharField(max_length=100, choices=method, blank=True, null=True)
    Bank_Name = models.CharField(max_length=100, blank=True, null=True)
    Cheque_Number = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(max_length=300, blank=True, null=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    @property
    def NetAmount(self):
        results = int(self.fee_type.Class_Amount) - int(self.discount.fees_discount.discountamount)
        return results

    @property
    def total_paid(self):
        results = PaidDues.objects.filter(student_id=self.student_id).aggregate(totals=models.Sum("paid_amount"))
        if (results['totals']):
            return results["totals"]
        else:
            return 0

    @property
    def DueAmount(self):
        results = self.NetAmount - self.total_paid
        return results

    @property
    def updatestatus(self):
        if (self.total_paid >= self.NetAmount):
            self.paid_status = self.paid
            self.save()
            return self.paid_status

        elif (self.total_paid == 0):
            self.paid_status = self.unpaid
            self.save()
            return self.paid_status

        elif (self.total_paid < self.NetAmount):
            self.paid_status = self.partial
            self.save()
            return self.paid_status

        else:
            return self.paid_status


class BulkInvoice(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    fee_type = models.CharField(max_length=100)
    student_name = models.CharField(max_length=100)
    IS = (('Yes', 'Yes'),
          ('No', 'No'))
    is_discount_applicable = models.CharField(max_length=100, blank=False, choices=IS)
    month = models.DateField(max_length=100)
    STATUS = (('Paid', 'Paid'),
              ('Pending', 'Pending'))
    paid_status = models.CharField(max_length=100, blank=False, choices=STATUS)
    note = models.TextField(max_length=300)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')


class DueFeeEmail(models.Model):
    PRO = (('Guardian', 'Guardian'),
           ('Student', 'Student'))
    receiver_role = models.CharField(max_length=100, blank=False, choices=PRO)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)

    due_fee_student = models.CharField(max_length=100)
    template = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    email_body = models.TextField(max_length=300)
    attachment = models.FileField(upload_to='attachment/', null=True, blank=False)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')


class DueFeeSMS(models.Model):
    PRO = (('Guardian', 'Guardian'),
           ('Student', 'Student'))
    receiver_type = models.CharField(max_length=100, blank=False, choices=PRO)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=False, null=True)
    due_fee_student = models.CharField(max_length=100)
    template = models.CharField(max_length=100)
    SMS = models.TextField(max_length=300)
    gateway = models.CharField(max_length=100)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')


class IncomeHead(models.Model):
    income_head = models.CharField(max_length=100)
    note = models.TextField(max_length=300)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.income_head


class Income(models.Model):
    INCOME_HEADS = 'IH'
    INCOME_METHODS = 'IM'
    report_options = [(INCOME_HEADS, 'Income_heads'), (INCOME_METHODS, 'Income_methods')]

    income_head = models.ForeignKey(IncomeHead, on_delete=models.CASCADE, blank=False, null=True)
    method = (('Cash', 'Cash'), ('Cheque', 'Cheque'))
    payment_method = models.CharField(max_length=100, choices=method)
    Bank_Name = models.CharField(max_length=100, blank=True, null=True)
    Cheque_Number = models.CharField(max_length=100, blank=True, null=True)
    amount = models.CharField(max_length=100)
    date = models.DateField(null=True)
    note = models.TextField(max_length=300)
    Reporting = models.CharField(max_length=100, choices=report_options, blank=True, null=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.income_head


class ExpenditureHead(models.Model):
    expenditure_head = models.CharField(max_length=100)
    note = models.TextField(max_length=300)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.expenditure_head


class Expenditure(models.Model):
    expenditure_head = models.ForeignKey(ExpenditureHead, on_delete=models.CASCADE, blank=False, null=True)
    method = (('Cash', 'Cash'), ('Cheque', 'Cheque'))
    expenditure_method = models.CharField(max_length=100, choices=method)
    Bank_Name = models.CharField(max_length=100, blank=True, null=True)
    Cheque_Number = models.CharField(max_length=100, blank=True, null=True)
    amount = models.CharField(max_length=100)
    date = models.DateField(null=True)
    note = models.TextField(max_length=300)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.expenditure_head


class Gallery(models.Model):
    gallery_title = models.CharField(max_length=100)
    note = models.TextField(max_length=300)
    IS = (('Yes', 'Yes'),
          ('No', 'No'))
    Is_View_on_Web = models.CharField(max_length=100, blank=False, choices=IS)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.gallery_title

    class Meta:
        verbose_name = _("Gallery")
        verbose_name_plural = _("Galleries")


class Image(models.Model):
    gallery_title = models.ForeignKey(Gallery, on_delete=models.CASCADE, blank=False, null=True)
    gallery_image = models.ImageField(upload_to='images/', null=True, blank=False)
    image_caption = models.CharField(max_length=100)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.image_caption


class Page(models.Model):
    IS = (('Header', 'Header'),
          ('Footer', 'Footer'))
    page_location = models.CharField(max_length=100, blank=False, choices=IS)
    page_title = models.CharField(max_length=100)
    page_description = models.TextField(max_length=300)
    page_image = models.ImageField(upload_to='images/', null=True, blank=False)
    modified = models.DateTimeField(verbose_name="Modified", auto_now=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.page_title


class Slider(models.Model):
    slider_image = models.ImageField(upload_to='sliders/', null=True, blank=False)
    image_title = models.CharField(max_length=100)
    modified = models.DateTimeField(verbose_name="Modified", auto_now=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.image_title


class About(models.Model):
    about_image = models.ImageField(upload_to='about/', null=True, blank=False)
    about = models.TextField(max_length=500)
    modified = models.DateTimeField(verbose_name="Modified", auto_now=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')
        verbose_name = _("About")
        verbose_name_plural = _("About")

    def __str__(self):
        return self.about


class Paypal(models.Model):
    paypal_email = models.CharField(max_length=100)
    is_demo = models.CharField(max_length=130, blank=False, choices=OPTIONS)
    paypal_extra_charge = models.CharField(max_length=100)
    is_active = models.CharField(max_length=130, blank=False, choices=OPTIONS)
    photo = models.ImageField(upload_to='avatars/', blank=False)

    def __str__(self):
        return self.paypal_email


class Airtel(models.Model):
    tel_no = models.CharField(max_length=100)
    is_active = models.CharField(max_length=130, blank=False, choices=OPTIONS)
    photo = models.ImageField(upload_to='avatars/', blank=False)

    def __str__(self):
        return self.tel_no

    class Meta:
        verbose_name = _("Airtel")
        verbose_name_plural = _("Airtel")


class MTN(models.Model):
    tel_no = models.CharField(max_length=100)
    is_active = models.CharField(max_length=130, blank=False, choices=OPTIONS)
    photo = models.ImageField(upload_to='avatars/', blank=False)

    def __str__(self):
        return self.tel_no

    class Meta:
        verbose_name = _("MTN")
        verbose_name_plural = _("MTN")


class Pesa(models.Model):
    tel_no = models.CharField(max_length=100)
    is_active = models.CharField(max_length=130, blank=False, choices=OPTIONS)
    photo = models.ImageField(upload_to='avatars/', blank=False)

    def __str__(self):
        return self.tel_no

    class Meta:
        verbose_name = _("Pesa")
        verbose_name_plural = _("Pesa")


class Payment(models.Model):
    paypal = models.ForeignKey(Paypal, on_delete=models.CASCADE, blank=False, null=True)
    airtel = models.ForeignKey(Airtel, on_delete=models.CASCADE, blank=False, null=True)
    MTN = models.ForeignKey(MTN, on_delete=models.CASCADE, blank=False, null=True)
    MPesa = models.ForeignKey(Pesa, on_delete=models.CASCADE, blank=False, null=True)

    # def __str__(self):
    #     return self.school


class ManageUser(models.Model):
    user_type = models.ForeignKey(Role, blank=False, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')


class SalaryPayment(models.Model):
    role_type = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False, null=True)
    payment_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')


class MonthlySalaryPaid(models.Model):
    academic_year = models.ForeignKey(Year, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    employees_id = models.CharField(max_length=100, default="id")
    employee = models.CharField(max_length=100)
    grade_name = models.CharField(max_length=100)
    basic_salary = models.CharField(max_length=100)
    house_rent = models.CharField(max_length=100)
    transport_allowance = models.CharField(max_length=100)
    medical_allowance = models.CharField(max_length=100)
    over_time_hourly_pay = models.CharField(max_length=100)
    provident_fund = models.CharField(max_length=100)
    hourly_rate = models.CharField(max_length=100)
    total_allowance = models.CharField(max_length=100)
    total_deduction = models.CharField(max_length=100)
    gross_salary = models.CharField(max_length=100)
    net_salary = models.CharField(max_length=100)
    over_time_total_hour = models.CharField(max_length=100)
    over_time_amount = models.CharField(max_length=100)
    Bonus = models.CharField(max_length=100)
    Penalty = models.CharField(max_length=100)
    Month = models.CharField(max_length=100)
    Payment_Method = models.CharField(max_length=100)
    Expenditure_Head = models.ForeignKey(ExpenditureHead, on_delete=models.CASCADE, blank=True, null=True)
    Bank_Name = models.CharField(max_length=100, blank=True, null=True)
    Cheque_Number = models.CharField(max_length=100, blank=True, null=True)
    note = models.CharField(max_length=100, blank=True, null=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')


class SMSTemplate(models.Model):
    receiver_type = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False, null=True)
    template_title = models.CharField(max_length=100)
    template = models.TextField(max_length=300)
    dynamic_tags = TaggableManager()

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')


class EmailTemplate(models.Model):
    receiver_type = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False, null=True)
    template_title = models.CharField(max_length=100)
    template = models.TextField(max_length=300)
    dynamic_tags = TaggableManager()

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')


class Purpose(models.Model):
    visitor_purpose = models.CharField(max_length=100)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.visitor_purpose


class Visitor(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    to_meet_user_type = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False, null=True)
    to_meet_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    visitor_purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE, blank=False, null=True)
    note = models.TextField(max_length=100)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.name


class Log(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    call_duration = models.CharField(max_length=100)
    call_date = models.DateField(max_length=100)
    follow_up = models.CharField(max_length=100)
    call_type = models.CharField(max_length=100, blank=False, choices=TYPES)
    note = models.TextField(max_length=100)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.name


class Dispatch(models.Model):
    to_Title = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    from_Title = models.CharField(max_length=100)
    dispatch_date = models.DateField(max_length=100)
    note = models.TextField(max_length=100)
    postal_Attachment = models.FileField(upload_to='attachments/', max_length=100)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    class Meta:
        verbose_name = _("Dispatch")
        verbose_name_plural = _("Dispatches")


class Receive(models.Model):
    to_Title = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    from_Title = models.CharField(max_length=100)
    receive_date = models.DateField(max_length=100)
    note = models.TextField(max_length=100)
    postal_Attachment = models.FileField(upload_to='attachments/', max_length=100)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.receive_date


class Leave(models.Model):
    applicant_type = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False, null=True)
    leave_Type = models.CharField(max_length=100)
    total_Leave = models.CharField(max_length=100)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.leave_Type


class Application(models.Model):
    applicant_type = models.ForeignKey(Role, on_delete=models.CASCADE, blank=False, null=True)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    leave_Type = models.ForeignKey(Leave, on_delete=models.CASCADE, blank=False, null=True)
    application_Date = models.DateField(max_length=100)
    leave_From = models.DateField(max_length=100)
    leave_To = models.DateField(max_length=100)
    status = models.CharField(max_length=100, default='New', choices=STATUS)
    leave_Reason = models.TextField(max_length=100)
    leave_attachment = models.FileField(upload_to='leave/', max_length=100)

    objects = models.Manager()

    class Meta:
        default_permissions = ('view', 'add', 'change', 'delete')

    def __str__(self):
        return self.status
