from django.forms import Textarea, TextInput, ChoiceField
from django.db import transaction
from schools.models import *
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, MonthPickerInput, DateTimePickerInput
from django.forms.widgets import CheckboxSelectMultiple, RadioSelect
from django.contrib.auth.forms import UserChangeForm

from django.db.models import Q

from django import forms


class SettingsForm(UserChangeForm):
    class Meta:
        model = Settings

        fields = ('brand_name', 'brand_title', 'language', 'enable_RTL', 'enable_Frontend', 'general_Theme',
                  'default_time_zone', 'date_format', 'brand_logo', 'favicon_icon', 'brand_footer',
                  'google_Analytics')

        widgets = {
            'date_format': DatePickerInput(),
        }


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School

        fields = ('school_name', 'school_code', 'address', 'phone', 'registration_date', 'email_address', 'fax',
                  'footer', 'currency', 'currency_symbol', 'enable_frontend', 'exam_final_result', 'latitude',
                  'longitude', 'facebook_url', 'twitter_url',
                  'online_Admission', 'api_key', 'linkedIn_url', 'google_plus_url', 'youtube_url', 'instagram_url',
                  'pinterest_url', 'status', 'frontend_Logo', 'backend_Logo', 'theme')

        widgets = {
            'school_name': TextInput(attrs={'placeholder': 'School Name'}),
            'school_code': TextInput(attrs={'placeholder': 'School Code'}),
            'address': TextInput(attrs={'placeholder': 'Address'}),
            'phone': TextInput(attrs={'placeholder': 'Phone'}),
            'email_address': TextInput(attrs={'placeholder': 'Email'}),
            'fax': TextInput(attrs={'placeholder': 'Fax'}),
            'footer': TextInput(attrs={'placeholder': 'Footer'}),
            'currency': TextInput(attrs={'placeholder': 'Currency'}),
            'currency_symbol': TextInput(attrs={'placeholder': 'Currency Symbol'}),
            'registration_date': DatePickerInput(),
        }


class EmailSettingsForm(forms.ModelForm):
    class Meta:
        model = EmailSetting

        fields = ('email_protocol', 'email_type', 'char_set', 'priority', 'email_from_name',
                  'email_from_address')


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ('role_name', 'note', 'is_default')


class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ('designation', 'note')


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('feedback', 'is_publish', 'date')

        widgets = {
            'feedback': Textarea(attrs={'cols': 30, 'rows': 2}),
            'date': DatePickerInput(),
        }


class UserForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['full_name', 'national_ID', 'phone', 'gender', 'blood_group', 'religion', 'birth_date',
                  'present_address', 'permanent_address', 'email', 'username', 'other_info', 'photo']
        # 'roles'

        widgets = {
            'full_name': TextInput(attrs={'placeholder': 'Name'}),
            'national_ID': TextInput(attrs={'placeholder': 'National ID'}),
            'phone': TextInput(attrs={'placeholder': 'Phone'}),
            'email': TextInput(attrs={'placeholder': 'Email'}),
            'religion': TextInput(attrs={'placeholder': 'Religion'}),
            'username': TextInput(attrs={'placeholder': 'Username'}),
            'present_address': Textarea(attrs={'cols': 30, 'rows': 2, 'placeholder': 'Present Address'}),
            'permanent_address': Textarea(attrs={'cols': 30, 'rows': 2, 'placeholder': 'Permanent Address'}),
            'other_info': Textarea(attrs={'cols': 30, 'rows': 2}),
            'birth_date': DatePickerInput(),
        }

        labels = {
            'full_name': 'Name',
        }

        error_messages = {
            'full_name': {
                'max_length': "Name can only be 25 characters in length"
            }
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'national_ID', 'phone', 'gender', 'blood_group', 'religion', 'birth_date',
                  'present_address', 'permanent_address', 'email', 'username', 'other_info', 'photo']

    widgets = {
        'birth_date': DatePickerInput(),
    }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'national_ID', 'phone', 'gender', 'blood_group', 'religion', 'birth_date',
                  'present_address', 'permanent_address', 'email', 'username', 'other_info', 'photo']

        widgets = {
            'other_info': Textarea(attrs={'cols': 30, 'rows': 2}),
            'birth_date': DatePickerInput(),
        }


class SuperuserForm(forms.ModelForm):
    class Meta:
        model = Superuser
        fields = ['roles', 'resume']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['roles'].queryset = Role.objects.filter(Q(role_name__startswith='Superuser'))

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(SuperuserForm, self).save(commit=False)
        user.is_superuser = True
        user.roles = 'Superuser'
        if commit:
            user.save()
        return user


class EditSuperuserForm(forms.ModelForm):
    class Meta:
        model = Superuser
        fields = ['roles', 'resume']


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['responsibility', 'salary_grade', 'salary_type', 'resume', 'Is_View_on_Web', 'roles',
                  'facebook_url', 'linkedIn_url', 'twitter_url', 'google_plus_url', 'instagram_url', 'youtube_url',
                  'pinterest_url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['roles'].queryset = Role.objects.filter(Q(role_name__startswith='Teacher'))

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(TeacherForm, self).save(commit=False)
        user.is_teacher = True
        user.roles = 'Teacher'
        if commit:
            user.save()
        return user


class EditTeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['responsibility', 'salary_grade', 'salary_type', 'resume', 'Is_View_on_Web', 'roles',
                  'facebook_url', 'linkedIn_url', 'twitter_url', 'google_plus_url', 'instagram_url', 'youtube_url',
                  'pinterest_url']


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['designation', 'salary_grade', 'salary_type', 'resume', 'Is_View_on_Web', 'roles',
                  'facebook_url', 'linkedIn_url', 'twitter_url', 'google_plus_url', 'instagram_url', 'youtube_url',
                  'pinterest_url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['roles'].queryset = Role.objects.exclude(Q(role_name__startswith='Superuser') |
                                                             Q(role_name__startswith='Teacher') |
                                                             Q(role_name__startswith='Student') |
                                                             Q(role_name__startswith='Guardian'))

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(EmployeeForm, self).save(commit=False)
        user.is_employee = True
        user.roles = 'Employee'
        if commit:
            user.save()
        return user


class EditEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['designation', 'salary_grade', 'salary_type', 'resume', 'Is_View_on_Web', 'roles',
                  'facebook_url', 'linkedIn_url', 'twitter_url', 'google_plus_url', 'instagram_url', 'youtube_url',
                  'pinterest_url']


class GuardianForm(forms.ModelForm):
    class Meta:
        model = Guardian
        fields = ['roles', 'profession']

    def save(self, commit=True):
        user = super(GuardianForm, self).save(commit=False)
        user.is_guardian = True
        user.roles = 'Guardian'
        if commit:
            user.save()
        return user


class EditGuardianForm(forms.ModelForm):
    class Meta:
        model = Guardian
        fields = ['roles', 'profession']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('admission_no', 'admission_date', 'guardian', 'relation_With_Guardian', 'classroom',
                  'section', 'group', 'roll_no', 'registration_no', 'roles', 'caste', 'student_type',
                  'fees_discount', 'second_language', 'previous_school', 'previous_class', 'transfer_certificate',
                  'father_name', 'father_phone', 'father_education', 'father_profession', 'father_designation',
                  'father_photo', 'mother_name', 'mother_phone', 'mother_education', 'mother_profession',
                  'mother_designation', 'mother_photo', 'health_condition')

        widgets = {
            'admission_no': TextInput(attrs={'placeholder': 'Admission No'}),
            'admission_date': DatePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['roles'].queryset = Role.objects.filter(Q(role_name__startswith='Student'))
        self.fields['section'].queryset = Section.objects.none()

        if 'classroom' in self.data:
            try:
                classroom_id = int(self.data.get('classroom'))
                self.fields['section'].queryset = Section.objects.filter(classroom_id=classroom_id).order_by(
                    'classroom')
            except (ValueError, TypeError):
                pass

        elif self.instance.pk:
            self.fields['section'].queryset = self.instance.classroom.section_set.order_by('section')

    def save(self, commit=True):
        user = super(StudentForm, self).save(commit=False)
        user.is_student = True
        user.roles = 'Student'
        if commit:
            user.save()
        return user


class EditStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('admission_no', 'admission_date', 'guardian', 'relation_With_Guardian', 'classroom',
                  'section', 'group', 'roll_no', 'registration_no', 'roles', 'caste', 'student_type',
                  'fees_discount', 'second_language', 'previous_school', 'previous_class', 'transfer_certificate',
                  'father_name', 'father_phone', 'father_education', 'father_profession', 'father_designation',
                  'father_photo', 'mother_name', 'mother_phone', 'mother_education', 'mother_profession',
                  'mother_designation', 'mother_photo', 'health_condition')

        widgets = {
            'admission_no': TextInput(attrs={'placeholder': 'Admission No'}),
            'admission_date': DatePickerInput(),
        }


class StudentTypeForm(forms.ModelForm):
    class Meta:
        model = StudentType
        fields = ('student_type', 'note')


class ManageCredentialForm(forms.ModelForm):
    class Meta:
        model = ManageUser
        fields = ('user_type', 'user',)

    def __init__(self, user_type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(
            roles=user_type
        )


class ManageUserForm(forms.ModelForm):
    class Meta:
        model = ManageUser
        fields = ('user_type', 'user',)

    def __init__(self, user_type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(
            roles=user_type
        )


class ActivityForm(forms.ModelForm):
    class Meta:
        model = ManageUser
        fields = ('user_type', 'user',)

    def __init__(self, user_type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(
            roles=user_type
        )


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ('classroom', 'numeric_name', 'class_teacher', 'note')


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('section', 'classroom', 'section_teacher', 'note')


class YearForm(forms.ModelForm):
    class Meta:
        model = Year
        fields = ('year', 'note')


class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ['term', 'is_current_term', 'year', 'next_term_begins']


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = (
            'subject_name', 'subject_code', 'subject_teacher', 'subject_unit', 'type', 'classroom', 'note', 'term')


class SyllabusForm(forms.ModelForm):
    class Meta:
        model = Syllabus
        fields = ('syllabus_title', 'classroom', 'subject_name', 'syllabus', 'note')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject_name'].queryset = Subject.objects.none()

        if 'classroom' in self.data:
            try:
                classroom_id = int(self.data.get('classroom'))
                self.fields['subject_name'].queryset = Subject.objects.filter(classroom_id=classroom_id).order_by(
                    'classroom')
            except (ValueError, TypeError):
                pass

        elif self.instance.pk:
            self.fields['subject_name'].queryset = self.instance.classroom.subject_set.order_by('subject_name')


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('material_title', 'classroom', 'subject', 'material', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.none()

        if 'classroom' in self.data:
            try:
                classroom_id = int(self.data.get('classroom'))
                self.fields['subject'].queryset = Subject.objects.filter(classroom_id=classroom_id).order_by(
                    'classroom')
            except (ValueError, TypeError):
                pass

        elif self.instance.pk:
            self.fields['subject'].queryset = self.instance.classroom.subject_set.order_by('subject')


class RoutineForm(forms.ModelForm):
    class Meta:
        model = Routine
        fields = ['classroom', 'section', 'subject_name', 'day', 'teacher', 'start_time', 'end_time',
                  'room_no']

    widgets = {
        'start_time': TimePickerInput(),
        'end_time': TimePickerInput(),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['section'].queryset = Section.objects.none()
        self.fields['subject_name'].queryset = Subject.objects.none()

        if 'classroom' in self.data:
            try:
                classroom_id = int(self.data.get('classroom'))
                self.fields['section'].queryset = Section.objects.filter(classroom_id=classroom_id).order_by(
                    'classroom')
                self.fields['subject_name'].queryset = Subject.objects.filter(classroom_id=classroom_id).order_by(
                    'classroom')
            except (ValueError, TypeError):
                pass

        elif self.instance.pk:
            self.fields['section'].queryset = self.instance.classroom.section_set.order_by('section')
            self.fields['subject_name'].queryset = self.instance.classroom.subject_set.order_by('subject_name')


class BulkStudentForm(forms.ModelForm):
    class Meta:
        model = BulkStudent
        fields = ('classroom', 'section')


# class StudentAttendanceForm(forms.ModelForm):
#     status = forms.ChoiceField(widget=forms.RadioSelect, choices=ATTENDANCE)
#
#     class Meta:
#         model = StudentAttendance
#         fields = ('classroom', 'section', 'date', 'student', 'status')
#
#         widgets = {
#             'date': DatePickerInput(),
#         }
#
#     def __init__(self, classroom=None, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['section'].queryset = Section.objects.filter(
#             classroom=classroom
#         )


class AttendanceForm(forms.Form):
    mark_attendance = forms.ChoiceField(widget=forms.RadioSelect, choices=ATTENDANCE)


class TeacherAttendanceForm(forms.ModelForm):
    status = forms.ChoiceField(widget=forms.RadioSelect, choices=ATTENDANCE)

    class Meta:
        model = TeacherAttendance
        fields = ('date', 'teacher', 'status')

        widgets = {
            'date': DatePickerInput(),
        }


class EmployeeAttendanceForm(forms.ModelForm):
    status = forms.ChoiceField(widget=forms.RadioSelect, choices=ATTENDANCE)

    class Meta:
        model = EmployeeAttendance
        fields = ('date', 'employee', 'status')

        widgets = {
            'date': DatePickerInput(),
        }


class AbsentEmailForm(forms.ModelForm):
    class Meta:
        model = AbsentEmail
        fields = ('receiver_type', 'absent_user', 'template', 'absent_date', 'subject', 'email_body')

        widgets = {
            'absent_date': DatePickerInput(),
        }


class AbsentSMSForm(forms.ModelForm):
    class Meta:
        model = AbsentSMS
        fields = ('receiver_type', 'absent_user', 'template', 'absent_date', 'gateway')

        widgets = {
            'absent_date': DatePickerInput(),
        }


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('assignment_title', 'classroom', 'subject', 'deadline', 'assignment', 'note')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.none()

        if 'classroom' in self.data:
            try:
                classroom_id = int(self.data.get('classroom'))
                self.fields['subject'].queryset = Subject.objects.filter(classroom_id=classroom_id).order_by(
                    'classroom')
            except (ValueError, TypeError):
                pass

        elif self.instance.pk:
            self.fields['subject'].queryset = self.instance.classroom.subject_set.order_by('subject')


class ExamGradeForm(forms.ModelForm):
    class Meta:
        model = ExamGrade
        fields = ('exam_grade', 'grade_point', 'mark_from', 'mark_to', 'note')


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ('exam_title', 'start_date', 'note')

        widgets = {
            'start_date': DatePickerInput(),
        }


class ExamScheduleForm(forms.ModelForm):
    class Meta:
        model = ExamSchedule
        fields = ('exam', 'classroom', 'subject', 'exam_date', 'start_time', 'end_time', 'room_no', 'note')

        widgets = {
            'exam_date': DatePickerInput(),
            'start_time': TimePickerInput(),
            'end_time': TimePickerInput(),
        }


class ExamSuggestionForm(forms.ModelForm):
    class Meta:
        model = ExamSuggestion
        fields = ('suggestion_title', 'exam', 'classroom', 'subject', 'suggestion', 'note')


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ('exam', 'classroom', 'section', 'subject', 'student')

    def __init__(self, classroom=None, section=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['exam'].queryset = Exam.objects.all()
        self.fields['classroom'].queryset = Classroom.objects.all()

        if classroom:
            self.fields['section'].queryset = Section.objects.filter(classroom=classroom)
            self.fields['subject'].queryset = Subject.objects.filter(classroom=classroom)

        else:
            self.fields['section'].queryset = Section.objects.none()
            self.fields['subject'].queryset = Subject.objects.none()


# class ScoreForm(forms.ModelForm):
#     class Meta:
#         model = Result
#         fields = ('year', 'term', 'gpa', 'cgpa', 'classroom', 'student')
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['year'].queryset = Year.objects.get(is_current_year=True)
#         self.fields['term'].queryset = Term.objects.get(is_current_term=True)
#         # self.fields['section'].queryset = Section.objects.filter(classroom=classroom)
#         # self.fields['subject'].queryset = Subject.objects.filter(classroom=classroom)
#         # self.fields['section'].queryset = Section.objects.none()
#         # self.fields['subject'].queryset = Subject.objects.none()


class ExamAttendanceForm(forms.ModelForm):
    class Meta:
        model = ExamAttendance
        fields = ('exam', 'classroom', 'section', 'subject')


class CertificateForm(forms.ModelForm):
    class Meta:
        model = CertificateType
        fields = ('certificate_name', 'school_name', 'certificate_text', 'footer_left_text',
                  'footer_middle_text', 'footer_right_text', 'background')


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('book_title', 'book_ID', 'ISBN_no', 'edition',
                  'author', 'language', 'price', 'quantity', 'almira_no', 'book_cover')


class EBookForm(forms.ModelForm):
    class Meta:
        model = EBook
        fields = (
            'classroom', 'subject', 'EBook_title', 'edition', 'author', 'language', 'cover_image', 'e_book')


class LibraryMemberForm(forms.ModelForm):
    class Meta:
        model = LibraryMember
        fields = ('photo', 'library_ID', 'name', 'classroom', 'section', 'roll_no')


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('select_book', 'library_member', 'ISBN_no', 'edition', 'author', 'language', 'price',
                  'quantity', 'almira_no', 'book_cover', 'return_date')

        widgets = {
            'return_date': DatePickerInput(),
        }


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ('vehicle_number', 'vehicle_model', 'driver', 'vehicle_licence', 'vehicle_contact', 'note')


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ('route_title', 'route_start', 'route_end', 'vehicle_for_route', 'stop_name', 'stop_km',
                  'stop_fare', 'note')


class TransportMemberForm(forms.ModelForm):
    class Meta:
        model = TransportMember
        fields = ('photo', 'name', 'classroom', 'section', 'roll_no', 'transport_route_name', 'stop_Name',
                  'stop_KM', 'stop_Fare')


class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ('hostel_name', 'hostel_type', 'address', 'note')


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('room_no', 'room_type', 'seat_total', 'hostel', 'cost_per_seat', 'note')


class HostelMemberForm(forms.ModelForm):
    class Meta:
        model = HostelMember
        fields = ('photo', 'name', 'classroom', 'section', 'roll_no', 'hostel_name', 'room_no',
                  'room_type')


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ('receiver_type', 'receiver', 'subject', 'email_body', 'attachment')


class SMSForm(forms.ModelForm):
    class Meta:
        model = SMS
        fields = ('receiver_type', 'receiver', 'SMS', 'gateway')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('receiver_type', 'recipient', 'subject', 'message')


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ('notice_title', 'date', 'notice_for', 'notice', 'Is_View_on_Web')

        widgets = {
            'date': DatePickerInput(),
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('news_title', 'date', 'image', 'news', 'Is_View_on_Web')

        widgets = {
            'date': DatePickerInput(),
        }


class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ('holiday_title', 'from_date', 'to_date', 'note', 'Is_View_on_Web')

        widgets = {
            'from_date': DatePickerInput(),
            'to_date': DatePickerInput(),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('event_title', 'event_for', 'event_place', 'from_date', 'to_date', 'image', 'note',
                  'Is_View_on_Web')

        widgets = {
            'from_date': DatePickerInput(),
            'to_date': DatePickerInput(),
        }


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ('name', 'phone', 'to_meet_user_type', 'to_meet_user', 'visitor_purpose',
                  # 'check_in',
                  'check_out', 'note')


class SalaryGradeForm(forms.ModelForm):
    class Meta:
        model = SalaryGrade
        fields = ('academic_year', 'school', 'payee', 'grade_name', 'basic_salary', 'house_rent', 'transport_allowance',
                  'medical_allowance',
                  'over_time_hourly_pay', 'provident_fund', 'hourly_rate', 'total_allowance', 'total_deduction',
                  'gross_salary', 'net_salary', 'over_time_total_hour', 'over_time_amount', 'Bonus', 'Penalty', 'Month',
                  'Payment_Method', 'Expenditure_Head', 'Cheque_Number', 'Bank_Name', 'note')

        widgets = {
            'note': Textarea(attrs={'cols': 30, 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.school:
            school_id = self.instance.school.pk
            self.fields['academic_year'].queryset = Year.objects.filter(school__id=school_id)


class SalaryPaymentForm(forms.ModelForm):
    class Meta:
        model = SalaryPayment
        fields = ('role_type', 'payment_to')

    def __init__(self, role_type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role_type'].queryset = Role.objects.exclude(Q(role_name__startswith='Superuser') |
                                                                 Q(role_name__startswith='Student') |
                                                                 Q(role_name__startswith='Guardian')).order_by('role_name')
        self.fields['payment_to'].queryset = User.objects.filter(
            roles=role_type
        )

        # if 'role' in self.data:
        #     try:
        #         rolesId = int(self.data.get('role'))
        #         self.fields['employee'].queryset = Employee.objects.filter(roles_id=rolesId).order_by(
        #             'user')
        #
        #     except (ValueError, TypeError):
        #         pass


class MonthlySalaryPaidForm(forms.ModelForm):
    class Meta:
        model = MonthlySalaryPaid
        fields = ('academic_year', 'employees_id', 'employee', 'grade_name', 'basic_salary',
                  'house_rent', 'transport_allowance', 'medical_allowance', 'over_time_hourly_pay',
                  'provident_fund', 'hourly_rate', 'total_allowance', 'total_deduction', 'gross_salary',
                  'net_salary', 'over_time_amount',)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['academic_year'].queryset = Year.objects.none()
    #     if 'school' in self.data:
    #         try:
    #             school_id = int(self.data.get('school'))
    #             self.fields['academic_year'].queryset =
    #             Year.objects.filter(school_id=school_id).order_by('start_month')
    #         except (ValueError, TypeError):
    #             pass


class PurposeForm(forms.ModelForm):
    class Meta:
        model = Purpose
        fields = ('visitor_purpose',)


class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ('name', 'phone', 'call_duration', 'call_date', 'follow_up', 'call_type', 'note')

        widgets = {
            'call_date': DatePickerInput(),
            'follow_up': DatePickerInput(),
        }


class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ('applicant_type', 'leave_Type', 'total_Leave')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['applicant_type'].queryset = Role.objects.exclude(Q(role_name__startswith='Guardian'))


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('applicant_type', 'applicant', 'leave_Type', 'application_Date', 'leave_From', 'leave_To',
                  'leave_Reason', 'leave_attachment')

        widgets = {
            'application_Date': DatePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['applicant_type'].queryset = Role.objects.exclude(Q(role_name__startswith='Guardian'))
        self.fields['applicant'].queryset = User.objects.none()

        if 'applicant_type' in self.data:
            try:
                applicant_type_id = int(self.data.get('applicant_type'))
                self.fields['applicant'].queryset = User.objects.filter(roles_id=applicant_type_id).order_by(
                    'applicant_type')
            except (ValueError, TypeError):
                pass

        elif self.instance.pk:
            self.fields['applicant'].queryset = self.instance.applicant_type.applicant_set.order_by('full_name')


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('border_color', 'top_background', 'card_school_name', 'school_name_font_size',
                  'school_name_color', 'school_address', 'school_address_color', 'admit_card_font_size',
                  'admit_card_color', 'admit_card_background', 'title_font_size', 'title_color', 'value_font_size',
                  'value_color', 'exam_font_size', 'exam_color', 'subject_font_size', 'subject_color',
                  'bottom_signature', 'signature_background', 'signature_color', 'signature_align', 'admit_card_logo')


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ('classroom', 'section', 'student', 'activity_date', 'activity')

        widgets = {
            'activity_date': DatePickerInput(),
        }


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discounting
        fields = ('title', 'amount', 'note')


class DispatchForm(forms.ModelForm):
    class Meta:
        model = Dispatch
        fields = (
            'to_Title', 'reference', 'address', 'from_Title', 'dispatch_date', 'note', 'postal_Attachment')

        widgets = {
            'birth_date': DatePickerInput(),
        }


class ManagePaymentForm(forms.Form):
    school = forms.ModelChoiceField(
        queryset=School.objects.all(),
        required=False
    )

    role = forms.ModelChoiceField(
        queryset=Role.objects.none(),
        required=False
    )

    user = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=False
    )

    grade = forms.ModelChoiceField(
        queryset=SalaryGrade.objects.all(),
        required=False
    )

    class Meta:
        fields = ('role', 'user', 'grade')

    def __init__(self, school=None, role=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].queryset = Role.objects.filter(school=school)
        if role:
            self.fields['user'].queryset = User.objects.filter(
                roles=role)


class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Receive
        fields = (
            'to_Title', 'reference', 'address', 'from_Title', 'receive_date', 'note', 'postal_Attachment')

        widgets = {
            'receive_date': DatePickerInput(),
        }


class FeeTypeForm(forms.ModelForm):
    class Meta:
        model = FeeType
        fields = ('fee_type', 'fee_title', 'note', 'Class', 'Class_Amount')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['Class'].queryset = Classroom.objects.none()
    #     if 'school' in self.data:
    #         try:
    #             school_id = int(self.data.get('school'))
    #             self.fields['Class'].queryset = Classroom.objects.filter(school_id=school_id).order_by('classroom')
    #         except (ValueError, TypeError):
    #             pass


class BulkInvoiceForm(forms.ModelForm):
    class Meta:
        model = BulkInvoice
        fields = ('classroom', 'fee_type', 'student_name', 'is_discount_applicable',
                  'month', 'paid_status', 'note')


class DueFeeEmailForm(forms.ModelForm):
    class Meta:
        model = DueFeeEmail
        fields = ('receiver_role', 'classroom', 'due_fee_student', 'template',
                  'subject', 'email_body', 'attachment')


class DueFeeSMSForm(forms.ModelForm):
    class Meta:
        model = DueFeeSMS
        fields = ('receiver_type', 'classroom', 'due_fee_student', 'template',
                  'SMS', 'gateway')


class IncomeHeadForm(forms.ModelForm):
    class Meta:
        model = IncomeHead
        fields = ('income_head', 'note')


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ('income_head', 'payment_method', 'amount', 'date', 'note')

        widgets = {
            'date': DatePickerInput(),
        }


class ExpenditureHeadForm(forms.ModelForm):
    class Meta:
        model = ExpenditureHead
        fields = ('expenditure_head', 'note')


class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = ('expenditure_head', 'expenditure_method', 'amount', 'date', 'note')

        widgets = {
            'date': DatePickerInput(),
        }


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ('gallery_title', 'note', 'Is_View_on_Web')


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('paypal', 'airtel', 'MTN', 'MPesa')


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('gallery_title', 'gallery_image', 'image_caption')


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('page_location', 'page_title', 'page_description', 'page_image')


class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ('slider_image', 'image_title')


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = '__all__'


class ComplainForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = ('complain_user_type', 'complain_user', 'complain_type', 'complain_date', 'complain',
                  'action_date')

        widgets = {
            'complain_date': DatePickerInput(),
            'action_date': DatePickerInput(),
        }


class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ('about', 'about_image')


class SMSTemplateForm(forms.ModelForm):
    class Meta:
        model = SMSTemplate
        fields = ('receiver_type', 'template_title', 'template', 'dynamic_tags')


class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = ('receiver_type', 'template_title', 'dynamic_tags', 'template')


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('paid_amount', 'discount', 'classroom', 'student', 'fee_type', 'fee_amount', 'month',
                  'paid_status', 'Payment_Method', 'Cheque_Number', 'Bank_Name', 'note', 'net_amount')
        widgets = {
            'note': Textarea(attrs={'cols': 30, 'rows': 2}),
            'month': MonthPickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['classroom'].queryset = Classroom.objects.none()
        self.fields['fee_type'].queryset = FeeType.objects.none()
        self.fields['student'].queryset = Student.objects.none()
        self.fields['fee_amount'].queryset = FeeType.objects.none()
        self.fields['discount'].queryset = Student.objects.none()

        if 'classroom' in self.data:
            try:
                classroom_id = int(self.data.get('classroom'))
                self.fields['student'].queryset = Student.objects.filter(classroom_id=classroom_id).order_by(
                    'classroom')
                self.fields['fee_type'].queryset = FeeType.objects.filter(Class_id=classroom_id).order_by(
                    'Class')
            except (ValueError, TypeError):
                pass


        elif self.instance.pk:
            self.fields['student'].queryset = self.instance.classroom.student_set.order_by('student')

        # loading discount for a student
        if 'student' in self.data:
            try:
                student_id = int(self.data.get('student'))
                self.fields['discount'].queryset = Student.objects.filter(id=student_id)
            except (ValueError, TypeError):
                pass

        if 'fee_type' in self.data:
            try:
                fee_type_id = int(self.data.get('fee_type'))
                self.fields['fee_amount'].queryset = FeeType.objects.filter(id=fee_type_id).order_by('Class_Amount')

            except (ValueError, TypeError):
                pass


class UpdateInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('paid_amount', 'Payment_Method', 'Cheque_Number', 'Bank_Name', 'note')
        widgets = {
            'note': Textarea(attrs={'cols': 30, 'rows': 2}),
            'month': MonthPickerInput(),
        }


class PaidDuesForm(forms.ModelForm):
    class Meta:
        model = PaidDues
        fields = ('student_id', 'paid_amount', 'classroom', 'student_name',
                  'Payment_Method', 'Cheque_Number', 'Bank_Name', 'note')


class SubjectRegistrationForm(forms.ModelForm):
    class Meta:
        model = TakenSubject
        fields = ('subject',)
        widgets = {
            'subject': forms.CheckboxSelectMultiple
        }


class PaidFeesForm(forms.ModelForm):
    class Meta:
        model = StudentPaidFees
        fields = ('student', 'paid_amount', 'paid_status', 'Payment_Method', 'note', 'Cheque_Number', 'Bank_Name')
        widgets = {
            'note': Textarea(attrs={'cols': 30, 'rows': 2})
        }
