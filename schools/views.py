import csv

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, UpdateView, ListView
from django.views.generic import View

from helpers import ajax_required
from .forms import *
from .models import *

IMAGE_FILE_TYPES = ['png', 'jpg', 'pjeg']


def web(request):
    return render(request, 'home/index_public.html')


def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password, backend='django.contrib.auth.backends.ModelBackend')
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "You have logged in successfully!")
                return render(request, 'home/home.html')
            else:
                messages.warning(request, "Your account has been disabled!")
                return render(request, 'home/login.html')
        else:
            messages.warning(request, "Invalid login!")
            return render(request, 'home/login.html')
    return render(request, 'home/login.html')


def logout_user(request):
    logout(request)
    return render(request, 'home/login.html')


def index(request):
    schools = School.objects.all()
    student_count = Student.objects.all().count()
    classroom_count = Classroom.objects.all().count()
    guardian_count = Guardian.objects.all().count()
    superuser_count = Superuser.objects.all().count()
    employee_count = Employee.objects.all().count()
    admin_count = Employee.objects.all().count()
    accountant_count = Employee.objects.all().count()
    librarian_count = Employee.objects.all().count()
    staff_count = Employee.objects.all().count()
    teacher_count = Teacher.objects.all().count()
    receptionist_count = Employee.objects.all().count()
    income_count = Income.objects.all().count()
    expenditure_count = Expenditure.objects.all().count()

    context = {
        'schools': schools,
        'student_count': student_count,
        'classroom_count': classroom_count,
        'guardian_count': guardian_count,
        'employee_count': employee_count,
        'superuser_count': superuser_count,
        'teacher_count': teacher_count,
        'admin_count': admin_count,
        'accountant_count': accountant_count,
        'librarian_count': librarian_count,
        'staff_count': staff_count,
        'receptionist_count': receptionist_count,
        'income_count': income_count,
        'expenditure_count': expenditure_count,
    }

    return render(request, 'home/home.html', context)

    # for school in School.objects.all():
    #     school_classrooms = school.classroom_set.all().count()
    #     school_students = school.student_set.all().count()
    #     school_teachers = school.teacher_set.all().count()
    #     school_employees = school.employee_set.all().count()
    #     school_incomes = school.income_set.all().count()
    #     school_expenditures = school.expenditure_set.all().count()
    #
    #     args = {
    #
    #         'school_classrooms': school_classrooms,
    #         'school_students': school_students,
    #         'school_teachers': school_teachers,
    #         'school_employees': school_employees,
    #         'school_incomes': school_incomes,
    #         'school_expenditures': school_expenditures,
    #     }


# #######################################===>BEGINNING OF PROFILE MODULE<===########################################


def view_profile(request):
    args = {'user': request.user}
    return render(request, 'profiles/profile.html', args)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST or None, request.FILES or None, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')

        else:
            form = EditProfileForm(instance=request.user)
            args = {'form': form}
            return render(request, 'profiles/update_profile.html', args)

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'profiles/update_profile.html', args)


class UserPasswordChangeView(LoginRequiredMixin, View):
    form_class = PasswordChangeForm
    template_name = 'profiles/change_password.html'

    def get(self, request):
        return render(request, self.template_name, {
            'form': self.form_class(request.user)
        })

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Password updated.'))
        return render(request, self.template_name, {'form': form})


# #######################################===>END OF PROFILE MODULE<===########################################

# #######################################===>BEGINNING OF SCHOOL MODULE<===########################################

class SchoolCreateView(CreateView):
    model = School
    template_name = 'schools/create_school.html'
    fields = ('school_name', 'school_code', 'address', 'phone', 'registration_date', 'email_address', 'fax',
              'footer', 'currency', 'currency_symbol', 'api_key',
              'online_Admission', 'enable_frontend', 'exam_final_result', 'latitude', 'longitude', 'facebook_url',
              'twitter_url', 'linkedIn_url', 'google_plus_url', 'youtube_url', 'instagram_url', 'pinterest_url',
              'status', 'frontend_Logo', 'backend_Logo', 'theme')

    def get_form(self):
        form = super().get_form()
        form.fields['registration_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        school = form.save(commit=False)
        school.save()
        return redirect('school_list')


class SchoolUpdateView(UpdateView):
    model = School
    template_name = 'schools/update_school.html'
    pk_url_kwarg = 'school_pk'
    fields = ('school_name', 'school_code', 'address', 'phone', 'registration_date', 'email_address', 'fax',
              'footer', 'currency', 'currency_symbol', 'api_key',
              'online_Admission', 'enable_frontend', 'exam_final_result', 'latitude', 'longitude', 'facebook_url',
              'twitter_url', 'linkedIn_url', 'google_plus_url', 'youtube_url', 'instagram_url', 'pinterest_url',
              'status', 'frontend_Logo', 'backend_Logo', 'theme')

    def get_form(self):
        form = super().get_form()
        form.fields['registration_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        school = form.save(commit=False)
        school.save()
        return redirect('school_list')


class SchoolListView(ListView):
    model = School
    template_name = 'schools/school_list.html'
    context_object_name = 'schools'


def save_school_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            schools = School.objects.all()
            data['html_school_list'] = render_to_string('schools/includes/partial_school_list.html', {
                'schools': schools
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def school_view(request, school_pk):
    school = get_object_or_404(School, pk=school_pk)
    if request.method == 'POST':
        form = SchoolForm(request.POST, instance=school)
    else:
        form = SchoolForm(instance=school)
    return save_school_form(request, form, 'schools/includes/partial_school_view.html')


def school_delete(request, school_pk):
    school = get_object_or_404(School, pk=school_pk)
    data = dict()
    if request.method == 'POST':
        school.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        schools = School.objects.all()
        data['html_school_list'] = render_to_string('schools/includes/partial_school_list.html', {
            'schools': schools
        })
    else:
        context = {'school': school}
        data['html_form'] = render_to_string('schools/includes/partial_school_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


class SchoolSettingView(UpdateView):
    model = School
    template_name = 'schools/school_setting.html'
    pk_url_kwarg = 'school_pk'
    fields = ('school_name', 'school_code', 'address', 'phone', 'registration_date', 'email_address', 'fax',
              'footer', 'currency', 'currency_symbol', 'session_start_month', 'session_end_month', 'api_key',
              'online_Admission', 'enable_frontend', 'exam_final_result', 'latitude', 'longitude', 'facebook_url',
              'twitter_url', 'linkedIn_url', 'google_plus_url', 'youtube_url', 'instagram_url', 'pinterest_url',
              'status', 'frontend_Logo', 'backend_Logo', 'theme')

    def get_form(self):
        form = super().get_form()
        form.fields['registration_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        school = form.save(commit=False)
        school.save()
        return redirect('school_list')


# #######################################===>END OF SCHOOL MODULE<===########################################

# #######################################===>BEGINNING OF CLASS MODULE<===###################################


class ClassroomListView(ListView):
    model = Classroom
    template_name = 'classrooms/classroom_list.html'
    context_object_name = 'classrooms'


class ClassroomCreateView(CreateView):
    model = Classroom
    template_name = 'classrooms/classroom_create.html'
    fields = ('classroom', 'numeric_name', 'class_teacher', 'note')

    def form_valid(self, form):
        classroom = form.save(commit=False)
        classroom.save()
        return redirect('classroom_list')


class ClassroomUpdateView(UpdateView):
    model = Classroom
    template_name = 'classrooms/classroom_update.html'
    pk_url_kwarg = 'classroom_pk'
    fields = ('classroom', 'numeric_name', 'class_teacher', 'note')

    def form_valid(self, form):
        classroom = form.save(commit=False)
        classroom.save()
        return redirect('classroom_list')


def save_classroom_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            classrooms = Classroom.objects.all()
            data['html_classroom_list'] = render_to_string('classrooms/includes/partial_classroom_list.html', {
                'classrooms': classrooms
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def classroom_delete(request, classroom_pk):
    classroom = get_object_or_404(Classroom, pk=classroom_pk)
    data = dict()
    if request.method == 'POST':
        classroom.delete()
        data['form_is_valid'] = True
        classrooms = Classroom.objects.all()
        data['html_classroom_list'] = render_to_string('classrooms/includes/partial_classroom_list.html', {
            'classrooms': classrooms
        })
    else:
        context = {'classroom': classroom}
        data['html_form'] = render_to_string('classrooms/includes/partial_classroom_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)

    # #######################################===>END OF CLASS MODULE<===########################################

    # #######################################===>BEGINNING OF SECTION MODULE<===###################################


class SectionListView(ListView):
    model = Section
    template_name = 'sections/section_list.html'
    context_object_name = 'sections'


def save_section_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            sections = Section.objects.all()
            data['html_section_list'] = render_to_string('sections/includes/partial_section_list.html', {
                'sections': sections
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


class SectionCreateView(CreateView):
    model = Section
    template_name = 'sections/section_create.html'
    fields = ('section', 'classroom', 'section_teacher', 'note')

    def form_valid(self, form):
        school = form.save(commit=False)
        school.save()
        return redirect('section_list')


class SectionUpdateView(UpdateView):
    model = Section
    template_name = 'sections/section_update.html'
    pk_url_kwarg = 'section_pk'
    fields = ('section', 'classroom', 'section_teacher', 'note')

    def form_valid(self, form):
        school = form.save(commit=False)
        school.save()
        return redirect('section_list')


def section_delete(request, section_pk):
    section = get_object_or_404(Section, pk=section_pk)
    data = dict()
    if request.method == 'POST':
        section.delete()
        data['form_is_valid'] = True
        sections = Section.objects.all()
        data['html_section_list'] = render_to_string('sections/includes/partial_section_list.html', {
            'sections': sections
        })
    else:
        context = {'section': section}
        data['html_form'] = render_to_string('sections/includes/partial_section_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)

    # #######################################===>END OF SECTION MODULE<===########################################

    # #######################################===>BEGINNING OF Email Setting MODULE<===################################


class EmailSettingsListView(ListView):
    model = EmailSetting
    template_name = 'emailsettings/emailsetting_list.html'
    context_object_name = 'emailsettings'


class EmailSettingsCreateView(CreateView):
    model = EmailSetting
    template_name = 'emailsettings/emailsetting_create.html'
    fields = ('email_protocol', 'email_type', 'char_set', 'priority', 'email_from_name',
              'email_from_address')

    def form_valid(self, form):
        emailsetting = form.save(commit=False)
        emailsetting.save()
        return redirect('emailsetting_list')


class EmailSettingsUpdateView(UpdateView):
    model = EmailSetting
    template_name = 'emailsettings/update_emailsetting.html'
    pk_url_kwarg = 'emailsetting_pk'
    fields = ('email_protocol', 'email_type', 'char_set', 'priority', 'email_from_name',
              'email_from_address')

    def form_valid(self, form):
        emailsetting = form.save(commit=False)
        emailsetting.save()
        return redirect('emailsetting_list')


def save_emailsetting_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            emailsettings = EmailSetting.objects.all()
            data['html_emailsetting_list'] = render_to_string('emailsettings/includes/partial_emailsetting_list.html', {
                'emailsettings': emailsettings
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def emailsetting_view(request, emailsetting_pk):
    emailsetting = get_object_or_404(EmailSetting, pk=emailsetting_pk)
    if request.method == 'POST':
        form = EmailSettingsForm(request.POST, instance=emailsetting)
    else:
        form = EmailSettingsForm(instance=emailsetting)
    return save_emailsetting_form(request, form, 'emailsettings/includes/partial_emailsetting_view.html')


def emailsetting_delete(request, emailsetting_pk):
    emailsetting = get_object_or_404(EmailSetting, pk=emailsetting_pk)
    data = dict()
    if request.method == 'POST':
        emailsetting.delete()
        data['form_is_valid'] = True
        emailsettings = emailsetting.objects.all()
        data['html_emailsetting_list'] = render_to_string('emailsettings/includes/partial_emailsetting_list.html', {
            'emailsettings': emailsettings
        })
    else:
        context = {'emailsetting': emailsetting}
        data['html_form'] = render_to_string('emailsettings/includes/partial_emailsetting_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF Email Setting MODULE<===######################################

# #######################################===>BEGINNING OF ROLE MODULE<===#########################################


class RoleListView(ListView):
    model = Role
    template_name = 'roles/role_list.html'
    context_object_name = 'roles'


class RoleCreateView(CreateView):
    model = Role
    template_name = 'roles/role_create.html'
    fields = ('role_name', 'note', 'is_default')

    def form_valid(self, form):
        role = form.save(commit=False)
        role.save()
        return redirect('role_list')


class RoleUpdateView(UpdateView):
    model = Role
    template_name = 'roles/update_role.html'
    pk_url_kwarg = 'role_pk'
    fields = ('role_name', 'note')

    def form_valid(self, form):
        role = form.save(commit=False)
        role.save()
        return redirect('role_list')


def save_role_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            roles = Role.objects.all()
            data['html_role_list'] = render_to_string('roles/includes/partial_role_list.html', {
                'roles': roles
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def role_delete(request, role_pk):
    role = get_object_or_404(Role, pk=role_pk)
    data = dict()
    if request.method == 'POST':
        role.delete()
        data['form_is_valid'] = True
        roles = Role.objects.all()
        data['html_role_list'] = render_to_string('roles/includes/partial_role_list.html', {
            'roles': roles
        })
    else:
        context = {'role': role}
        data['html_form'] = render_to_string('roles/includes/partial_role_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF ROLE MODULE<===##############################################

# #######################################===>BEGINNING OF SUPERUSER MODULE<===###################################


class SuperuserListView(ListView):
    model = Superuser
    template_name = 'superusers/superuser_list.html'
    context_object_name = 'superusers'


def save_superuser_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            superusers = Superuser.objects.all()
            data['html_superuser_list'] = render_to_string('superusers/includes/partial_superuser_list.html', {
                'superusers': superusers
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def superuser_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST or None, request.FILES or None)
        superuser_form = SuperuserForm(request.POST or None, request.FILES or None)

        if form.is_valid() and superuser_form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = True
            user.save()

            user.superuser.roles = superuser_form.cleaned_data.get('roles')
            user.superuser.resume = superuser_form.cleaned_data.get('resume')
            user.superuser.save()

            return redirect('superuser_list')

    else:
        form = UserForm()
        superuser_form = SuperuserForm()

    context = {
        'form': form,
        'superuser_form': superuser_form
    }
    return render(request, 'superusers/superuser_create.html', context)


def superuser_update(request, superuser_pk):
    user = get_object_or_404(User, pk=superuser_pk)

    if request.method == "POST":
        form = EditUserForm(request.POST, request.FILES, instance=user)
        superuser_form = EditSuperuserForm(request.POST, request.FILES, instance=user.superuser)

        if form.is_valid() and superuser_form.is_valid():
            user_form = form.save()
            custom_form = superuser_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('superuser_list')

        else:
            form = EditUserForm(instance=user)
            superuser_form = EditSuperuserForm(instance=user.superuser)

            args = {
                'form': form,
                'superuser_form': superuser_form
            }
            return render(request, 'superusers/superuser_update.html', args)

    else:
        form = EditUserForm(instance=user)
        superuser_form = EditSuperuserForm(instance=user.superuser)

        args = {
            'form': form,
            'superuser_form': superuser_form
        }
        return render(request, 'superusers/superuser_update.html', args)


def superuser_view(request, superuser_pk):
    superuser = get_object_or_404(Superuser, pk=superuser_pk)
    if request.method == 'POST':
        form = SuperuserForm(request.POST, instance=superuser)
    else:
        form = SuperuserForm(instance=superuser)
    return save_superuser_form(request, form, 'superusers/includes/partial_superuser_view.html')


def superuser_delete(request, superuser_pk):
    superuser = get_object_or_404(Superuser, pk=superuser_pk)
    data = dict()
    if request.method == 'POST':
        superuser.delete()
        data['form_is_valid'] = True
        superusers = Superuser.objects.all()
        data['html_superuser_list'] = render_to_string('superusers/includes/partial_superuser_list.html', {
            'superusers': superusers
        })
    else:
        context = {'superuser': superuser}
        data['html_form'] = render_to_string('superusers/includes/partial_superuser_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF SUPERUSER MODULE<===######################################


# #######################################===>BEGINNING OF MANAGE USER MODULE<===######################################

def manage_user(request):
    context = {}

    role = request.POST.get('user_type')
    context['form'] = ManageUserForm(role)
    # Filter
    q = request.POST.get('user')
    if q:
        q = q.replace('.', '')
        users = User.objects.filter(id=str(q))
        context['users'] = users

    return render(request, 'users/manage_users.html', context)


def user_deactivate(request, user_pk):
    user = User.objects.get(pk=user_pk)
    user.is_active = False
    user.save()
    messages.success(request, "User account has been successfully deactivated!")
    return redirect('manage_users')


def user_activate(request, user_pk):
    user = User.objects.get(pk=user_pk)
    user.is_active = True
    user.save()
    messages.success(request, "User account has been successfully activated!")
    return redirect('manage_users')


# #######################################===>END OF MANAGE USER MODULE<===######################################

# #######################################===>BEGINNING OF BACKUP MODULE<===##################################

def backup(request):
    return render(request, 'backup/backup.html')


# #######################################===>END OF BACKUP MODULE<===######################################

# #######################################===>BEGINNING OF USER CREDENTIAL MODULE<===##################################


def manage_credential(request):
    context = {}

    role = request.POST.get('user_type')
    context['form'] = ManageCredentialForm(role)
    # Filter
    users = request.POST.get('user')
    if users:
        users = users.replace('.', '')
        users = User.objects.filter(id=str(users))
        context['users'] = users

    return render(request, 'users/credentials.html', context)


# #######################################===>END OF USER CREDENTIAL MODULE<===######################################

# #######################################===>BEGINNING OF ACTIVITY LOG MODULE<===##################################


def activity(request):
    context = {}

    role = request.POST.get('user_type')
    context['form'] = ManageUserForm(role)
    # Filter
    users = request.POST.get('user')
    if users:
        users = users.replace('.', '')
        users = User.objects.filter(id=str(users))
        context['users'] = users

    return render(request, 'users/activity.html', context)


# #######################################===>END OF ACTIVITY LOG MODULE<===######################################

# ####################################===>BEGINNING OF FEEDBACK MODULE<===########################################


class FeedbackListView(ListView):
    model = Feedback
    template_name = 'feedbacks/feedback_list.html'
    context_object_name = 'feedbacks'


# class FeedbackCreateView(CreateView):
#     model = Feedback
#     template_name = 'feedbacks/feedback_create.html'
#     fields = ('feedback', 'is_publish', 'date')
#
#     def form_valid(self, form):
#         feedback = form.save(commit=False)
#         feedback.save()
#         return redirect('feedback_list')


def publish(request, feedback_pk):
    feedback = Feedback.objects.get(pk=feedback_pk)
    feedback.is_publish = 'Yes'
    feedback.save()
    messages.success(request, "Feedback account has been successfully deactivated!")
    return redirect('feedback_list')


def unpublish(request, feedback_pk):
    feedback = Feedback.objects.get(pk=feedback_pk)
    feedback.is_publish = 'No'
    feedback.save()
    messages.success(request, "Feedback account has been successfully activated!")
    return redirect('feedback_list')


class FeedbackUpdateView(UpdateView):
    model = Feedback
    template_name = 'feedbacks/update_feedback.html'
    pk_url_kwarg = 'feedback_pk'
    fields = ('feedback', 'is_publish', 'date')

    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        feedback = form.save(commit=False)
        feedback.save()
        return redirect('feedback_list')


def save_feedback_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            feedbacks = Feedback.objects.all()
            data['html_feedback_list'] = render_to_string('feedbacks/includes/partial_feedback_list.html', {
                'feedbacks': feedbacks
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def feedback_delete(request, feedback_pk):
    feedback = get_object_or_404(Feedback, pk=feedback_pk)
    data = dict()
    if request.method == 'POST':
        feedback.delete()
        data['form_is_valid'] = True
        feedbacks = Feedback.objects.all()
        data['html_feedback_list'] = render_to_string('feedbacks/includes/partial_feedback_list.html', {
            'feedbacks': feedbacks
        })
    else:
        context = {'feedback': feedback}
        data['html_form'] = render_to_string('feedbacks/includes/partial_feedback_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# ####################################### ===>END OF FEEDBACK MODULE<===########################################

# #######################################===>BEGINNING OF STUDENT MODULE<===######################################


class StudentListView(ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'


class OnlineStudentListView(ListView):
    model = Student
    template_name = 'students/online_list.html'
    context_object_name = 'students'


def save_student_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            students = Student.objects.all()
            data['html_student_list'] = render_to_string('students/includes/partial_student_list.html', {
                'students': students
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def student_create(request):
    form = UserForm(request.POST or None, request.FILES or None)
    student_form = StudentForm(request.POST or None, request.FILES or None)

    if form.is_valid() and student_form.is_valid():
        user = form.save(commit=False)
        user.is_student = True
        user.save()

        user.student.admission_no = student_form.cleaned_data.get('admission_no')
        user.student.admission_date = student_form.cleaned_data.get('admission_date')
        user.student.guardian = student_form.cleaned_data.get('guardian')
        user.student.relation_With_Guardian = student_form.cleaned_data.get('relation_With_Guardian')
        user.student.classroom = student_form.cleaned_data.get('classroom')
        user.student.section = student_form.cleaned_data.get('section')
        user.student.group = student_form.cleaned_data.get('group')
        user.student.roll_no = student_form.cleaned_data.get('roll_no')
        user.student.registration_no = student_form.cleaned_data.get('registration_no')
        user.student.roles = student_form.cleaned_data.get('roles')
        user.student.discount = student_form.cleaned_data.get('fees_discount')
        user.student.second_language = student_form.cleaned_data.get('second_language')
        user.student.previous_school = student_form.cleaned_data.get('previous_school')
        user.student.previous_class = student_form.cleaned_data.get('previous_class')
        user.student.transfer_certificate = student_form.cleaned_data.get('transfer_certificate')
        user.student.father_name = student_form.cleaned_data.get('father_name')
        user.student.father_phone = student_form.cleaned_data.get('father_phone')
        user.student.father_education = student_form.cleaned_data.get('father_education')
        user.student.father_profession = student_form.cleaned_data.get('father_profession')
        user.student.father_designation = student_form.cleaned_data.get('father_designation')
        user.student.father_photo = student_form.cleaned_data.get('father_photo')
        user.student.mother_name = student_form.cleaned_data.get('mother_name')
        user.student.mother_phone = student_form.cleaned_data.get('mother_phone')
        user.student.mother_education = student_form.cleaned_data.get('mother_education')
        user.student.mother_profession = student_form.cleaned_data.get('mother_profession')
        user.student.mother_designation = student_form.cleaned_data.get('mother_designation')
        user.student.mother_photo = student_form.cleaned_data.get('mother_photo')
        user.student.health_condition = student_form.cleaned_data.get('health_condition')
        user.student.save()

        student_url = reverse('student_list')
        return redirect(student_url)
    context = {
        'form': form,
        'student_form': student_form,
    }
    return render(request, 'students/student_create.html', context)


def student_view(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
    else:
        form = StudentForm(instance=student)
    return save_student_form(request, form, 'students/includes/partial_student_view.html')


def student_update(request, student_pk):
    user = get_object_or_404(User, pk=student_pk)

    if request.method == "POST":
        form = EditUserForm(request.POST, request.FILES, instance=user)
        student_form = EditStudentForm(request.POST, request.FILES, instance=user.student)

        if form.is_valid() and student_form.is_valid():
            user_form = form.save()
            custom_form = student_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('student_list')

        else:
            form = EditUserForm(instance=user)
            student_form = EditStudentForm(instance=user.student)

            args = {
                'form': form,
                'student_form': student_form
            }
            return render(request, 'students/student_update.html', args)

    else:
        form = EditUserForm(instance=user)
        student_form = EditStudentForm(instance=user.student)

        args = {
            'form': form,
            'student_form': student_form
        }
        return render(request, 'students/student_update.html', args)


def student_delete(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    data = dict()
    if request.method == 'POST':
        student.delete()
        data['form_is_valid'] = True
        students = student.objects.all()
        data['html_student_list'] = render_to_string('students/includes/partial_student_list.html', {
            'students': students
        })
    else:
        context = {'student': student}
        data['html_form'] = render_to_string('students/includes/partial_student_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF STUDENT MODULE<===##########################################

# #######################################===>BEGINNING OF GUARDIAN MODULE<===####################################


def guardian_list(request, guardian_pk=None):
    if guardian_pk:
        guardians = Guardian.objects.get(pk=guardian_pk)
        students = Student.objects.filter(guardian_id=guardian_pk).order_by('full_name')
    else:
        guardians = Guardian.objects.all()
        students = Student.objects.all()

    return render(request, 'guardians/guardian_list.html', {
        'guardians': guardians,
        'students': students
    })


def save_guardian_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            guardians = Guardian.objects.all()
            data['html_guardian_list'] = render_to_string('guardians/includes/partial_guardian_list.html', {
                'guardians': guardians
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def guardian_create(request):
    form = UserForm(request.POST or None, request.FILES or None)
    guardian_form = GuardianForm(request.POST or None, request.FILES or None)

    if form.is_valid() and guardian_form.is_valid():
        user = form.save(commit=False)
        user.is_guardian = True
        user.save()

        user.guardians.school = guardian_form.cleaned_data.get('school')
        user.guardians.roles = guardian_form.cleaned_data.get('roles')
        user.guardians.profession = guardian_form.cleaned_data.get('profession')
        user.guardians.save()

        guardian_url = reverse('guardian_list')
        return redirect(guardian_url)

    context = {
        'form': form,
        'guardian_form': guardian_form,
    }
    return render(request, 'guardians/guardian_create.html', context)


def guardian_view(request, guardian_pk):
    guardian = get_object_or_404(Guardian, pk=guardian_pk)
    if request.method == 'POST':
        form = GuardianForm(request.POST, instance=guardian)
    else:
        form = GuardianForm(instance=guardian)
    return save_guardian_form(request, form, 'guardians/includes/partial_guardian_view.html')


def guardian_update(request, guardian_pk):
    user = get_object_or_404(User, pk=guardian_pk)

    if request.method == "POST":
        form = EditUserForm(request.POST, request.FILES, instance=user)
        guardian_form = EditGuardianForm(request.POST, request.FILES, instance=user.guardians)

        if form.is_valid() and guardian_form.is_valid():
            user_form = form.save()
            custom_form = guardian_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('guardian_list')

        else:
            form = EditUserForm(instance=user)
            guardian_form = EditGuardianForm(instance=user.guardians)

            args = {
                'form': form,
                'guardian_form': guardian_form
            }
            return render(request, 'guardians/guardian_update.html', args)

    else:
        form = EditUserForm(instance=user)
        guardian_form = EditGuardianForm(instance=user.guardians)

        args = {
            'form': form,
            'guardian_form': guardian_form
        }
        return render(request, 'guardians/guardian_update.html', args)


def guardian_delete(request, guardian_pk):
    guardian = get_object_or_404(Guardian, pk=guardian_pk)
    data = dict()
    if request.method == 'POST':
        guardian.delete()
        data['form_is_valid'] = True
        guardians = Guardian.objects.all()
        data['html_guardian_list'] = render_to_string('guardians/includes/partial_guardian_list.html', {
            'guardians': guardians
        })
    else:
        context = {'guardian': guardian}
        data['html_form'] = render_to_string('guardians/includes/partial_guardian_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# ####################################===>END OF GUARDIAN MODULE<===##############################################

# ####################################===>BEGINNING OF DESIGNATION MODULE<===#####################################


class DesignationListView(ListView):
    model = Designation
    template_name = 'designations/designation_list.html'
    context_object_name = 'designations'


class DesignationCreateView(CreateView):
    model = Designation
    template_name = 'designations/designation_create.html'
    fields = ('designation', 'note')

    def form_valid(self, form):
        designation = form.save(commit=False)
        designation.save()
        return redirect('designation_list')


class DesignationUpdateView(UpdateView):
    model = Designation
    template_name = 'designations/update_designation.html'
    pk_url_kwarg = 'designation_pk'
    fields = ('designation', 'note')

    def form_valid(self, form):
        designation = form.save(commit=False)
        designation.save()
        return redirect('designation_list')


def save_designation_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            designations = Designation.objects.all()
            data['html_designation_list'] = render_to_string('designations/includes/partial_designation_list.html', {
                'designations': designations
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def designation_delete(request, designation_pk):
    designation = get_object_or_404(Designation, pk=designation_pk)
    data = dict()
    if request.method == 'POST':
        designation.delete()
        data['form_is_valid'] = True
        designations = Designation.objects.all()
        data['html_designation_list'] = render_to_string('designations/includes/partial_designation_list.html', {
            'designations': designations
        })
    else:
        context = {'designation': designation}
        data['html_form'] = render_to_string('designations/includes/partial_designation_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# ####################################### ===>END OF DESIGNATION MODULE<===########################################

# ####################################===>BEGINNING OF EMAIL TEMPLATE MODULE<===#####################################


class EmailtemplateListView(ListView):
    model = EmailTemplate
    template_name = 'emailtemplates/emailtemplate_list.html'
    context_object_name = 'emailtemplates'


class EmailtemplateCreateView(CreateView):
    model = EmailTemplate
    template_name = 'emailtemplates/emailtemplate_create.html'
    fields = ('receiver_type', 'template_title', 'template', 'dynamic_tags')

    def form_valid(self, form):
        emailtemplate = form.save(commit=False)
        emailtemplate.save()
        return redirect('emailtemplate_list')


class EmailtemplateUpdateView(UpdateView):
    model = EmailTemplate
    template_name = 'emailtemplates/update_emailtemplate.html'
    pk_url_kwarg = 'emailtemplate_pk'
    fields = ('receiver_type', 'template_title', 'template', 'dynamic_tags')

    def form_valid(self, form):
        emailtemplate = form.save(commit=False)
        emailtemplate.save()
        return redirect('emailtemplate_list')


def save_emailtemplate_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            emailtemplates = EmailTemplate.objects.all()
            data['html_emailtemplate_list'] = render_to_string(
                'emailtemplates/includes/partial_emailtemplate_list.html',
                {
                    'emailtemplates': emailtemplates
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def emailtemplate_delete(request, emailtemplate_pk):
    emailtemplate = get_object_or_404(EmailTemplate, pk=emailtemplate_pk)
    data = dict()
    if request.method == 'POST':
        emailtemplate.delete()
        data['form_is_valid'] = True
        emailtemplates = EmailTemplate.objects.all()
        data['html_emailtemplate_list'] = render_to_string('emailtemplates/includes/partial_emailtemplate_list.html', {
            'emailtemplates': emailtemplates
        })
    else:
        context = {'emailtemplate': emailtemplate}
        data['html_form'] = render_to_string('emailtemplates/includes/partial_emailtemplate_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# ####################################### ===>END OF EMAIL TEMPLATE MODULE<===########################################

# ####################################===>BEGINNING OF SMS TEMPLATE MODULE<===#####################################


class SmstemplateListView(ListView):
    model = SMSTemplate
    template_name = 'smstemplates/smstemplate_list.html'
    context_object_name = 'smstemplates'


class SmstemplateCreateView(CreateView):
    model = SMSTemplate
    template_name = 'smstemplates/smstemplate_create.html'
    fields = ('receiver_type', 'template_title', 'template', 'dynamic_tags')

    def form_valid(self, form):
        smstemplate = form.save(commit=False)
        smstemplate.save()
        return redirect('smstemplate_list')


class SmstemplateUpdateView(UpdateView):
    model = SMSTemplate
    template_name = 'smstemplates/update_smstemplate.html'
    pk_url_kwarg = 'smstemplate_pk'
    fields = ('receiver_type', 'template_title', 'template', 'dynamic_tags')

    def form_valid(self, form):
        smstemplate = form.save(commit=False)
        smstemplate.save()
        return redirect('smstemplate_list')


def save_smstemplate_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            smstemplates = SMSTemplate.objects.all()
            data['html_smstemplate_list'] = render_to_string(
                'smstemplates/includes/partial_smstemplate_list.html', {
                    'smstemplates': smstemplates
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def smstemplate_delete(request, smstemplate_pk):
    smstemplate = get_object_or_404(SMSTemplate, pk=smstemplate_pk)
    data = dict()
    if request.method == 'POST':
        smstemplate.delete()
        data['form_is_valid'] = True
        smstemplates = SMSTemplate.objects.all()
        data['html_smstemplate_list'] = render_to_string('smstemplates/includes/partial_smstemplate_list.html', {
            'smstemplates': smstemplates
        })
    else:
        context = {'smstemplate': smstemplate}
        data['html_form'] = render_to_string('smstemplates/includes/partial_smstemplate_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# ####################################### ===>END OF SMS TEMPLATE MODULE<===########################################

# #######################################===>BEGINNING OF LOG MODULE<===#####################################


class LogListView(ListView):
    model = Log
    template_name = 'log/log_list.html'
    context_object_name = 'log'


class LogCreateView(CreateView):
    model = Log
    template_name = 'log/log_create.html'
    fields = ('name', 'phone', 'call_duration', 'call_date', 'follow_up', 'call_type', 'note')

    def get_form(self):
        form = super().get_form()
        form.fields['call_date'].widget = DatePickerInput()
        form.fields['follow_up'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        log = form.save(commit=False)
        log.save()
        return redirect('log_list')


class LogUpdateView(UpdateView):
    model = Log
    template_name = 'log/update_log.html'
    pk_url_kwarg = 'log_pk'
    fields = ('name', 'phone', 'call_duration', 'call_date', 'follow_up', 'call_type', 'note')

    def get_form(self):
        form = super().get_form()
        form.fields['call_date'].widget = DatePickerInput()
        form.fields['follow_up'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        log = form.save(commit=False)
        log.save()
        return redirect('log_list')


def log_view(request, log_pk):
    log = get_object_or_404(Log, pk=log_pk)
    if request.method == 'POST':
        form = LogForm(request.POST, instance=log)
    else:
        form = LogForm(instance=log)
    return save_log_form(request, form, 'log/includes/partial_log_view.html')


def save_log_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            logs = Log.objects.all()
            data['html_log_list'] = render_to_string('log/includes/partial_log_list.html', {
                'logs': logs
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def log_delete(request, log_pk):
    log = get_object_or_404(Log, pk=log_pk)
    data = dict()
    if request.method == 'POST':
        log.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        logs = Log.objects.all()
        data['html_log_list'] = render_to_string('log/includes/partial_log_list.html', {
            'logs': logs
        })
    else:
        context = {'log': log}
        data['html_form'] = render_to_string('log/includes/partial_log_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF LOG MODULE<===#####################################

# #######################################===>BEGINNING OF EMPLOYEE MODULE<===######################################


class EmployeeListView(ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'


def save_employee_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            employees = Employee.objects.all()
            data['html_employee_list'] = render_to_string('employees/includes/partial_employee_list.html', {
                'employees': employees
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def employee_create(request):
    form = UserForm(request.POST or None, request.FILES or None)
    employee_form = EmployeeForm(request.POST or None, request.FILES or None)

    if form.is_valid() and employee_form.is_valid():
        user = form.save(commit=False)
        user.is_employee = True
        user.save()

        user.employee.designation = employee_form.cleaned_data.get('designation')
        user.employee.salary_grade = employee_form.cleaned_data.get('salary_grade')
        user.employee.salary_type = employee_form.cleaned_data.get('salary_type')
        user.employee.roles = employee_form.cleaned_data.get('roles')
        user.employee.resume = employee_form.cleaned_data.get('resume')
        user.employee.Is_View_on_Web = employee_form.cleaned_data.get('Is_View_on_Web')
        user.employee.facebook_url = employee_form.cleaned_data.get('facebook_url')
        user.employee.linkedIn_url = employee_form.cleaned_data.get('linkedIn_url')
        user.employee.twitter_url = employee_form.cleaned_data.get('twitter_url')
        user.employee.google_plus_url = employee_form.cleaned_data.get('google_plus_url')
        user.employee.instagram_url = employee_form.cleaned_data.get('instagram_url')
        user.employee.youtube_url = employee_form.cleaned_data.get('youtube_url')
        user.employee.pinterest_url = employee_form.cleaned_data.get('pinterest_url')
        user.employee.save()

        employee_url = reverse('employee_list')
        return redirect(employee_url)

    context = {
        'form': form,
        'employee_form': employee_form,
    }
    return render(request, 'employees/employee_create.html', context)


def employee_view(request, employee_pk):
    employee = get_object_or_404(Employee, pk=employee_pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
    else:
        form = EmployeeForm(instance=employee)
    return save_employee_form(request, form, 'employees/includes/partial_employee_view.html')


def employee_update(request, employee_pk):
    user = get_object_or_404(User, pk=employee_pk)

    if request.method == "POST":
        form = EditUserForm(request.POST, request.FILES, instance=user)
        employee_form = EditEmployeeForm(request.POST, request.FILES, instance=user.employee)

        if form.is_valid() and employee_form.is_valid():
            user_form = form.save()
            custom_form = employee_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('employee_list')

        else:
            form = EditUserForm(instance=user)
            employee_form = EditEmployeeForm(instance=user.employee)

            args = {
                'form': form,
                'employee_form': employee_form
            }
            return render(request, 'employees/employee_update.html', args)

    else:
        form = EditUserForm(instance=user)
        employee_form = EditEmployeeForm(instance=user.employee)

        args = {
            'form': form,
            'employee_form': employee_form
        }
        return render(request, 'employees/employee_update.html', args)


# class EmployeeUpdateView(UpdateView):
#     model = Employee
#     template_name = 'employees/employee_update.html'
#     pk_url_kwarg = 'employee_pk'
#     fields = ('designation', 'salary_grade', 'salary_type', 'resume', 'Is_View_on_Web', 'roles',
#                   'facebook_url', 'linkedIn_url', 'twitter_url', 'google_plus_url', 'instagram_url', 'youtube_url',
#                   'pinterest_url')
#
#     def form_valid(self, form):
#         employee = form.save(commit=False)
#         employee.save()
#         return redirect('employee_list')


def employee_delete(request, employee_pk):
    employee = get_object_or_404(Employee, pk=employee_pk)
    data = dict()
    if request.method == 'POST':
        employee.delete()
        data['form_is_valid'] = True
        employees = Employee.objects.all()
        data['html_employee_list'] = render_to_string('employees/includes/partial_employee_list.html', {
            'employees': employees
        })
    else:
        context = {'employee': employee}
        data['html_form'] = render_to_string('employees/includes/partial_employee_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)

    # #######################################===>END OF EMPLOYEE MODULE<===########################################

    # ###################################===>BEGINNING OF ACADEMIC YEAR MODULE<===###################################


class AcademicYearListView(ListView):
    model = Year
    template_name = 'years/year_list.html'
    context_object_name = 'years'


# class AcademicYearCreateView(CreateView):
#     model = Year
#     template_name = 'years/year_create.html'
#     fields = ('year', 'is_running', 'note')
#
#     def get_form(self):
#         form = super().get_form()
#         form.fields['start_month'].widget = MonthPickerInput()
#         form.fields['end_month'].widget = MonthPickerInput()
#         return form
#
#     def form_valid(self, form):
#         year = form.save(commit=False)
#         year.save()
#         return redirect('year_list')


def year_create(request):
    if request.method == 'POST':
        form = YearForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Academic Year created successfully ! ')

    else:
        form = YearForm()
    return render(request, 'years/year_create.html', {'form': form})


def year_update(request, year_pk):
    year = Year.objects.get(pk=year_pk)
    if request.method == 'POST':
        a = request.POST.get('is_current_year')
        if a == '2':
            unset = Year.objects.get(is_current_year=True)
            unset.is_current_year = False
            unset.save()
            form = YearForm(request.POST, instance=year)
            if form.is_valid():
                form.save()
                messages.success(request, 'Year updated successfully ! ')
        else:
            form = YearForm(request.POST, instance=year)
            if form.is_valid():
                form.save()
                messages.success(request, 'Year updated successfully ! ')
                return redirect('year_list')
    else:
        form = YearForm(instance=year)
    return render(request, 'years/year_update.html', {'form': form})


def save_year_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            years = Year.objects.all()
            data['html_year_list'] = render_to_string('years/includes/partial_year_list.html', {
                'years': years
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def year_delete(request, year_pk):
    year = get_object_or_404(Year, pk=year_pk)
    data = dict()
    if request.method == 'POST':
        if year.is_current_year == True:
            messages.info(request, "You cannot delete current session")
            return redirect('year_list')
        else:
            year.delete()
            data['form_is_valid'] = True
            years = Year.objects.all()
            data['html_year_list'] = render_to_string('years/includes/partial_year_list.html', {
                'years': years
            })
    else:
        context = {'year': year}
        data['html_form'] = render_to_string('years/includes/partial_year_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# ###################################===>END OF Academic YEAR MODULE<===###################################

# ###################################===>BEGINNING OF TERM MODULE<===###################################


def term_list(request):
    terms = Term.objects.all().order_by('-term')
    return render(request, 'terms/term_list.html', {"terms": terms, })


def term_create(request):
    if request.method == 'POST':
        form = TermForm(request.POST)
        if form.is_valid():
            data = form.data.get('is_current_term')  # returns string of 'True' if the user selected Yes
            if data == 'True':
                term = form.data.get('term')
                ss = form.data.get('year')
                year = Year.objects.get(pk=ss)
                try:
                    if Term.objects.get(term=term, year=ss):
                        messages.info(request, term + " term in " + year.year + " year already exist")
                        return redirect('create_new_term')
                except:
                    term = Term.objects.get(is_current_term=True)
                    term.is_current_term = False
                    term.save()
                    form.save()
            form.save()
            messages.success(request, 'Term added successfully ! ')
            return redirect('term_list')
    else:
        form = TermForm()
    return render(request, 'terms/term_create.html', {'form': form})


def term_update(request, term_pk):
    term = Term.objects.get(pk=term_pk)
    if request.method == 'POST':
        if request.POST.get(
                'is_current_term') == 'True':  # returns string of 'True' if the user selected yes for 'is current term'
            unset_term = Term.objects.get(is_current_term=True)
            unset_term.is_current_term = False
            unset_term.save()
            unset_year = Year.objects.get(is_current_year=True)
            unset_year.is_current_year = False
            unset_year.save()
            new_year = request.POST.get('year')
            form = TermForm(request.POST, instance=term)
            if form.is_valid():
                set_year = Year.objects.get(pk=new_year)
                set_year.is_current_year = True
                set_year.save()
                form.save()
                messages.success(request, 'Term updated successfully !')
                return redirect('term_list')
        else:
            form = TermForm(request.POST, instance=term)
            if form.is_valid():
                form.save()
                return redirect('term_list')

    else:
        form = TermForm(instance=term)
    return render(request, 'terms/term_update.html', {'form': form})


def term_delete(request, term_pk):
    term = get_object_or_404(Term, pk=term_pk)
    if term.is_current_term == True:
        messages.info(request, "You cannot delete current term")
        return redirect('term_list')
    else:
        term.delete()
        messages.success(request, "Term successfully deleted")
    return redirect('term_list')


# ######################################===>END OF TERM MODULE<===#################################

# ######################################===>BEGINNING OF TEACHER MODULE<===#################################


class TeacherListView(ListView):
    model = Teacher
    template_name = 'teachers/teacher_list.html'
    context_object_name = 'teachers'


def save_teacher_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            teachers = Teacher.objects.all()
            data['html_teacher_list'] = render_to_string('teachers/includes/partial_teacher_list.html', {
                'teachers': teachers
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def teacher_create(request):
    form = UserForm(request.POST or None, request.FILES or None)
    teacher_form = TeacherForm(request.POST or None, request.FILES or None)

    if form.is_valid() and teacher_form.is_valid():
        user = form.save(commit=False)
        user.is_teacher = True
        user.save()

        user.teacher.responsibility = teacher_form.cleaned_data.get('responsibility')
        user.teacher.salary_grade = teacher_form.cleaned_data.get('salary_grade')
        user.teacher.salary_type = teacher_form.cleaned_data.get('salary_type')
        user.teacher.roles = teacher_form.cleaned_data.get('roles')
        user.teacher.resume = teacher_form.cleaned_data.get('resume')
        user.teacher.Is_View_on_Web = teacher_form.cleaned_data.get('Is_View_on_Web')
        user.teacher.facebook_url = teacher_form.cleaned_data.get('facebook_url')
        user.teacher.linkedIn_url = teacher_form.cleaned_data.get('linkedIn_url')
        user.teacher.twitter_url = teacher_form.cleaned_data.get('twitter_url')
        user.teacher.google_plus_url = teacher_form.cleaned_data.get('google_plus_url')
        user.teacher.instagram_url = teacher_form.cleaned_data.get('instagram_url')
        user.teacher.youtube_url = teacher_form.cleaned_data.get('youtube_url')
        user.teacher.pinterest_url = teacher_form.cleaned_data.get('pinterest_url')
        user.teacher.save()

        teacher_url = reverse('teacher_list')
        return redirect(teacher_url)

    context = {
        'form': form,
        'teacher_form': teacher_form,
    }
    return render(request, 'teachers/teacher_create.html', context)


def teacher_view(request, teacher_pk):
    teacher = get_object_or_404(Teacher, pk=teacher_pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
    else:
        form = TeacherForm(instance=teacher)
    return save_teacher_form(request, form, 'teachers/includes/partial_teacher_view.html')


def teacher_update(request, teacher_pk):
    user = get_object_or_404(User, pk=teacher_pk)

    if request.method == "POST":
        form = EditUserForm(request.POST, request.FILES, instance=user)
        teacher_form = EditTeacherForm(request.POST, request.FILES, instance=user.teacher)

        if form.is_valid() and teacher_form.is_valid():
            user_form = form.save()
            custom_form = teacher_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('teacher_list')

        else:
            form = EditUserForm(instance=user)
            teacher_form = EditTeacherForm(instance=user.teacher)

            args = {
                'form': form,
                'teacher_form': teacher_form
            }
            return render(request, 'teachers/teacher_update.html', args)

    else:
        form = EditUserForm(instance=user)
        teacher_form = EditTeacherForm(instance=user.teacher)

        args = {
            'form': form,
            'teacher_form': teacher_form
        }
        return render(request, 'teachers/teacher_update.html', args)


def teacher_delete(request, teacher_pk):
    teacher = get_object_or_404(Teacher, pk=teacher_pk)
    data = dict()
    if request.method == 'POST':
        teacher.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        teachers = Teacher.objects.all()
        data['html_teacher_list'] = \
            render_to_string(
                'teachers/includes/partial_teacher_list.html', {
                    'teachers': teachers
                })
    else:
        context = {'teacher': teacher}
        data['html_form'] = \
            render_to_string(
                'teachers/includes/partial_teacher_delete.html',
                context,
                request=request,
            )
    return JsonResponse(data)


# #######################################===>END OF TEACHER MODULE<===###############################################

# #######################################===>BEGINNING OF STUDENT TYPE MODULE<===#####################################


class StudentTypeListView(ListView):
    model = StudentType
    template_name = 'student_types/student_type_list.html'
    context_object_name = 'student_types'


class StudentTypeCreateView(CreateView):
    model = StudentType
    template_name = 'student_types/student_type_create.html'
    fields = ('student_type', 'note')

    def form_valid(self, form):
        student_type = form.save(commit=False)
        student_type.save()
        return redirect('student_type_list')


class StudentTypeUpdateView(UpdateView):
    model = StudentType
    template_name = 'student_types/student_type_update.html'
    pk_url_kwarg = 'student_type_pk'
    fields = ('student_type', 'note')

    def form_valid(self, form):
        student_type = form.save(commit=False)
        student_type.save()
        return redirect('student_type_list')


def save_student_type_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            student_types = StudentType.objects.all()
            data['html_student_type_list'] = render_to_string('student_types/includes/partial_student_type_list.html', {
                'student_types': student_types
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def student_type_delete(request, student_type_pk):
    student_type = get_object_or_404(StudentType, pk=student_type_pk)
    data = dict()
    if request.method == 'POST':
        student_type.delete()
        data['form_is_valid'] = True
        student_types = StudentType.objects.all()
        data['html_student_type_list'] = render_to_string('student_types/includes/partial_student_type_list.html', {
            'student_types': student_types
        })
    else:
        context = {'student_type': student_type}
        data['html_form'] = render_to_string('student_types/includes/partial_student_type_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF STUDENT TYPE MODULE<===#####################################


# #######################################===>BEGINNING OF ACTIVITY MODULE<===#####################################


class ActivityListView(ListView):
    model = Activity
    template_name = 'activity/activity_list.html'
    context_object_name = 'activity'


class ActivityCreateView(CreateView):
    model = Activity
    template_name = 'activity/activity_create.html'
    fields = ('classroom', 'section', 'student', 'activity_date', 'activity')

    def get_form(self):
        form = super().get_form()
        form.fields['activity_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        activity = form.save(commit=False)
        activity.save()
        return redirect('activity_list')


class ActivityUpdateView(UpdateView):
    model = Activity
    template_name = 'activity/update_activity.html'
    pk_url_kwarg = 'activity_pk'
    fields = ('classroom', 'section', 'student', 'activity_date', 'activity')

    def get_form(self):
        form = super().get_form()
        form.fields['activity_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        activity = form.save(commit=False)
        activity.save()
        return redirect('activity_list')


def activity_view(request, activity_pk):
    activity = get_object_or_404(Activity, pk=activity_pk)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
    else:
        form = ActivityForm(instance=activity)
    return save_activity_form(request, form, 'activity/includes/partial_activity_view.html')


def save_activity_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            activitys = Activity.objects.all()
            data['html_activity_list'] = render_to_string('activity/includes/partial_activity_list.html', {
                'activitys': activitys
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def activity_delete(request, activity_pk):
    activity = get_object_or_404(Activity, pk=activity_pk)
    data = dict()
    if request.method == 'POST':
        activity.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        activitys = Activity.objects.all()
        data['html_activity_list'] = render_to_string('activity/includes/partial_activity_list.html', {
            'activitys': activitys
        })
    else:
        context = {'activity': activity}
        data['html_form'] = render_to_string('activity/includes/partial_activity_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF ACTIVITY MODULE<===##########################################

# #######################################===>BEGINNING OF SYLLABUS MODULE<===#####################################


class SyllabusListView(ListView):
    model = Syllabus
    template_name = 'syllabus/syllabus_list.html'
    context_object_name = 'syllabus'


def syllabus_create(request):
    form = SyllabusForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        syllabus = form.save(commit=False)

        syllabus.syllabus_title = form.cleaned_data.get('syllabus_title')
        syllabus.classroom = form.cleaned_data.get('classroom')
        syllabus.subject_name = form.cleaned_data.get('subject_name')
        syllabus.syllabus = form.cleaned_data.get('syllabus')
        syllabus.note = form.cleaned_data.get('note')

        syllabus.save()

        syllabus_url = reverse('syllabus_list')
        return redirect(syllabus_url)

    context = {
        'form': form,
    }
    return render(request, 'syllabus/syllabus_create.html', context)


class SyllabusUpdateView(UpdateView):
    model = Syllabus
    template_name = 'syllabus/update_syllabus.html'
    pk_url_kwarg = 'syllabus_pk'
    fields = ('syllabus_title', 'classroom', 'subject_name', 'syllabus', 'note')

    def form_valid(self, form):
        syllabus = form.save(commit=False)
        syllabus.save()
        return redirect('syllabus_list')


def syllabus_view(request, syllabus_pk):
    syllabus = get_object_or_404(Syllabus, pk=syllabus_pk)
    if request.method == 'POST':
        form = SyllabusForm(request.POST, instance=syllabus)
    else:
        form = SyllabusForm(instance=syllabus)
    return save_syllabus_form(request, form, 'syllabus/includes/partial_syllabus_view.html')


def save_syllabus_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            syllabuss = Syllabus.objects.all()
            data['html_syllabus_list'] = render_to_string('syllabus/includes/partial_syllabus_list.html', {
                'syllabuss': syllabuss
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def syllabus_delete(request, syllabus_pk):
    syllabus = get_object_or_404(Syllabus, pk=syllabus_pk)
    data = dict()
    if request.method == 'POST':
        syllabus.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        syllabuss = Syllabus.objects.all()
        data['html_syllabus_list'] = render_to_string('syllabus/includes/partial_syllabus_list.html', {
            'syllabuss': syllabuss
        })
    else:
        context = {'syllabus': syllabus}
        data['html_form'] = render_to_string('syllabus/includes/partial_syllabus_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF SYLLABUS MODULE<===##########################################

# #######################################===>BEGINNING OF CARD MODULE<===#####################################


class CardListView(ListView):
    model = Card
    template_name = 'card/card_list.html'
    context_object_name = 'cards'


class CardCreateView(CreateView):
    model = Card
    template_name = 'card/card_create.html'
    fields = ('border_color', 'top_background', 'card_school_name', 'school_name_font_size',
              'school_name_color', 'school_address', 'school_address_color', 'admit_card_font_size',
              'admit_card_color', 'admit_card_background', 'title_font_size', 'title_color', 'value_font_size',
              'value_color', 'exam_font_size', 'exam_color', 'subject_font_size', 'subject_color',
              'bottom_signature', 'signature_background', 'signature_color', 'signature_align', 'admit_card_logo')

    def form_valid(self, form):
        card = form.save(commit=False)
        card.save()
        return redirect('card_list')


class CardUpdateView(UpdateView):
    model = Card
    template_name = 'card/update_card.html'
    pk_url_kwarg = 'card_pk'
    fields = ('border_color', 'top_background', 'card_school_name', 'school_name_font_size',
              'school_name_color', 'school_address', 'school_address_color', 'admit_card_font_size',
              'admit_card_color', 'admit_card_background', 'title_font_size', 'title_color', 'value_font_size',
              'value_color', 'exam_font_size', 'exam_color', 'subject_font_size', 'subject_color',
              'bottom_signature', 'signature_background', 'signature_color', 'signature_align', 'admit_card_logo')

    def form_valid(self, form):
        card = form.save(commit=False)
        card.save()
        return redirect('card_list')


def card_view(request, card_pk):
    card = get_object_or_404(Card, pk=card_pk)
    if request.method == 'POST':
        form = CardForm(request.POST, instance=card)
    else:
        form = CardForm(instance=card)
    return save_card_form(request, form, 'card/includes/partial_card_view.html')


def save_card_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            cards = Card.objects.all()
            data['html_card_list'] = render_to_string('card/includes/partial_card_list.html', {
                'cards': cards
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def card_delete(request, card_pk):
    card = get_object_or_404(Card, pk=card_pk)
    data = dict()
    if request.method == 'POST':
        card.delete()
        data['form_is_valid'] = True
        cards = Card.objects.all()
        data['html_card_list'] = render_to_string('card/includes/partial_card_list.html', {
            'cards': cards
        })
    else:
        context = {'card': card}
        data['html_form'] = render_to_string('card/includes/partial_card_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF CARD MODULE<===##########################################

# #######################################===>BEGINNING OF ADMIT MODULE<===#####################################


class AdmitListView(ListView):
    model = Card
    template_name = 'card/card_list.html'
    context_object_name = 'cards'


class AdmitCreateView(CreateView):
    model = Card
    template_name = 'card/card_create.html'
    fields = ('border_color', 'top_background', 'card_school_name', 'school_name_font_size',
              'school_name_color', 'school_address', 'school_address_color', 'admit_card_font_size',
              'admit_card_color', 'admit_card_background', 'title_font_size', 'title_color', 'value_font_size',
              'value_color', 'exam_font_size', 'exam_color', 'subject_font_size', 'subject_color',
              'bottom_signature', 'signature_background', 'signature_color', 'signature_align', 'admit_card_logo')

    def form_valid(self, form):
        card = form.save(commit=False)
        card.save()
        return redirect('card_list')


class AdmitUpdateView(UpdateView):
    model = Card
    template_name = 'card/update_card.html'
    pk_url_kwarg = 'admit_pk'
    fields = ('border_color', 'top_background', 'card_school_name', 'school_name_font_size',
              'school_name_color', 'school_address', 'school_address_color', 'admit_card_font_size',
              'admit_card_color', 'admit_card_background', 'title_font_size', 'title_color', 'value_font_size',
              'value_color', 'exam_font_size', 'exam_color', 'subject_font_size', 'subject_color',
              'bottom_signature', 'signature_background', 'signature_color', 'signature_align', 'admit_card_logo')

    def form_valid(self, form):
        card = form.save(commit=False)
        card.save()
        return redirect('card_list')


def admit_view(request, admit_pk):
    card = get_object_or_404(Card, pk=admit_pk)
    if request.method == 'POST':
        form = CardForm(request.POST, instance=card)
    else:
        form = CardForm(instance=card)
    return save_card_form(request, form, 'card/includes/partial_card_view.html')


def admit_delete(request, admit_pk):
    card = get_object_or_404(Card, pk=admit_pk)
    data = dict()
    if request.method == 'POST':
        card.delete()
        data['form_is_valid'] = True
        cards = Card.objects.all()
        data['html_card_list'] = render_to_string('card/includes/partial_card_list.html', {
            'cards': cards
        })
    else:
        context = {'card': card}
        data['html_form'] = render_to_string('card/includes/partial_card_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF ADMIT MODULE<===##########################################

# #######################################===>BEGINNING OF MATERIAL MODULE<===#####################################


class MaterialListView(ListView):
    model = Material
    template_name = 'material/material_list.html'
    context_object_name = 'material'


def material_create(request):
    form = MaterialForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        material = form.save(commit=False)

        material.material_title = form.cleaned_data.get('material_title')
        material.classroom = form.cleaned_data.get('classroom')
        material.subject = form.cleaned_data.get('subject')
        material.material = form.cleaned_data.get('material')
        material.description = form.cleaned_data.get('description')

        material.save()

        material_url = reverse('material_list')
        return redirect(material_url)

    context = {
        'form': form,
    }
    return render(request, 'material/material_create.html', context)


class MaterialUpdateView(UpdateView):
    model = Material
    template_name = 'material/update_material.html'
    pk_url_kwarg = 'material_pk'
    fields = ('material_title', 'classroom', 'subject', 'material', 'description')

    def form_valid(self, form):
        material = form.save(commit=False)
        material.save()
        return redirect('material_list')


def material_view(request, material_pk):
    material = get_object_or_404(Material, pk=material_pk)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
    else:
        form = MaterialForm(instance=material)
    return save_material_form(request, form, 'material/includes/partial_material_view.html')


def save_material_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            materials = Material.objects.all()
            data['html_material_list'] = render_to_string('material/includes/partial_material_list.html', {
                'materials': materials
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def material_delete(request, material_pk):
    material = get_object_or_404(Material, pk=material_pk)
    data = dict()
    if request.method == 'POST':
        material.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        materials = Material.objects.all()
        data['html_material_list'] = render_to_string('material/includes/partial_material_list.html', {
            'materials': materials
        })
    else:
        context = {'material': material}
        data['html_form'] = render_to_string('material/includes/partial_material_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF MATERIAL MODULE<===#####################################

# #######################################===>BEGINNING OF SUBJECT MODULE<===#####################################

class SubjectListView(ListView):
    model = Subject
    template_name = 'subjects/subject_list.html'
    context_object_name = 'subjects'


class SubjectCreateView(CreateView):
    model = Subject
    template_name = 'subjects/subject_create.html'
    fields = ('subject_name', 'subject_code', 'subject_teacher', 'subject_unit', 'type', 'classroom', 'term', 'note')

    def form_valid(self, form):
        subject = form.save(commit=False)
        subject.save()
        return redirect('subject_list')


class SubjectUpdateView(UpdateView):
    model = Subject
    template_name = 'subjects/update_subject.html'
    pk_url_kwarg = 'subject_pk'
    fields = ('subject_name', 'subject_code', 'subject_teacher', 'type', 'classroom', 'subject_unit', 'term', 'note')

    def form_valid(self, form):
        subject = form.save(commit=False)
        subject.save()
        return redirect('subject_list')


def subject_view(request, subject_pk):
    subject = get_object_or_404(Subject, pk=subject_pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
    else:
        form = SubjectForm(instance=subject)
    return save_subject_form(request, form, 'subjects/includes/partial_subject_view.html')


def save_subject_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            subjects = Subject.objects.all()
            data['html_subject_list'] = render_to_string('subjects/includes/partial_subject_list.html', {
                'subjects': subjects
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def subject_delete(request, subject_pk):
    subject = get_object_or_404(Subject, pk=subject_pk)
    data = dict()
    if request.method == 'POST':
        subject.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        subjects = Subject.objects.all()
        data['html_subject_list'] = render_to_string('subjects/includes/partial_subject_list.html', {
            'subjects': subjects
        })
    else:
        context = {'subject': subject}
        data['html_form'] = render_to_string('subjects/includes/partial_subject_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


def subject_registration(request):
    if request.method == 'POST':
        ids = ()
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None)  # remove csrf_token
        for key in data.keys():
            ids = ids + (str(key),)
        for s in range(0, len(ids)):
            student = Student.objects.get(user__pk=request.user.id)
            subject = Subject.objects.get(pk=ids[s])
            obj = TakenSubject.objects.create(student=student, subject=subject)
            obj.save()
            messages.success(request, 'Subjects Registered Successfully!')
        return redirect('subject_register')
    else:
        student = Student.objects.get(user_id=request.user.pk)
        taken_subjects = TakenSubject.objects.filter(student__user__id=request.user.id)
        t = ()
        for i in taken_subjects:
            t += (i.subject.pk,)
        current_term = Term.objects.get(is_current_term=True)
        subjects = Subject.objects.filter(classroom=student.classroom).exclude(id__in=t)
        all_subjects = Subject.objects.filter(classroom=student.classroom)

        no_subject_is_registered = False  # Check if no subject is registered
        all_subjects_are_registered = False

        registered_subjects = Subject.objects.filter(classroom=student.classroom).filter(id__in=t)
        if registered_subjects.count() == 0:  # Check if number of registered subjects is 0
            no_subject_is_registered = True

        if registered_subjects.count() == all_subjects.count():
            all_subjects_are_registered = True

        total_first_term_unit = 0
        total_sec_term_unit = 0
        total_registered_unit = 0
        for i in subjects:
            if i.term == "First":
                total_first_term_unit += int(i.subject_unit)
            if i.term == "Second":
                total_sec_term_unit += int(i.subject_unit)
        for i in registered_subjects:
            total_registered_unit += int(i.subject_unit)
        context = {
            "all_subjects_are_registered": all_subjects_are_registered,
            "no_subject_is_registered": no_subject_is_registered,
            "current_term": current_term,
            "subjects": subjects,
            "total_first_term_unit": total_first_term_unit,
            "total_sec_term_unit": total_sec_term_unit,
            "registered_subjects": registered_subjects,
            "total_registered_unit": total_registered_unit,
            "student": student,
        }
        return render(request, 'subjects/subject_registration.html', context)


def subject_drop(request):
    if request.method == 'POST':
        ids = ()
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None)  # remove csrf_token
        for key in data.keys():
            ids = ids + (str(key),)
        for s in range(0, len(ids)):
            student = Student.objects.get(user__pk=request.user.id)
            subject = Subject.objects.get(pk=ids[s])
            obj = TakenSubject.objects.get(student=student, subject=subject)
            obj.delete()
            messages.success(request, 'Successfully Dropped!')
        return redirect('subject_register')


# #######################################===>END OF SUBJECT MODULE<===##########################################

# #######################################===>BEGINNING OF ROUTINE MODULE<===#####################################


def routine_list(request):
    schools = School.objects.all()
    classrooms = Classroom.objects.all()

    # Filters
    classrooms_filter = request.POST.get('classroom')

    schedule_dict = dict()
    if classrooms_filter:
        schedule = Routine.objects.filter(section__classroom=classrooms_filter).distinct().prefetch_related(
            'teacher')

        if schedule:
            for day in DAYS_OF_THE_WEEK:
                schedule_dict[day[1]] = schedule.filter(day=day[0])
    context = {
        'TimeList': TimeList,
        'days': DAYS_OF_THE_WEEK[0:5],
        'schedule': schedule_dict,
        'classrooms': classrooms,
        'schools': schools,
    }
    return render(request, 'routines/routine_list.html', context)


def save_routine_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            routines = Routine.objects.all()
            data['html_routine_list'] = render_to_string('routines/includes/partial_routine_list.html', {
                'routines': routines
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def routine_create(request):
    form = RoutineForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        routine = form.save(commit=False)

        routine.classroom = form.cleaned_data.get('classroom')
        routine.section = form.cleaned_data.get('section')
        routine.subject_name = form.cleaned_data.get('subject_name')
        routine.day = form.cleaned_data.get('day')
        routine.teacher = form.cleaned_data.get('teacher')
        routine.start_time = form.cleaned_data.get('start_time')
        routine.end_time = form.cleaned_data.get('end_time')
        routine.room_no = form.cleaned_data.get('room_no')

        routine.save()

        routine_url = reverse('routine_list')
        return redirect(routine_url)

    context = {
        'form': form,
    }
    return render(request, 'routines/routine_create.html', context)


class RoutineUpdateView(UpdateView):
    model = Routine
    template_name = 'routines/update_routine.html'
    pk_url_kwarg = 'routine_pk'
    fields = ('classroom', 'section', 'subject_name', 'day', 'teacher', 'start_time', 'end_time', 'room_no')

    def get_form(self):
        form = super().get_form()
        form.fields['start_time'].widget = TimePickerInput()
        form.fields['end_time'].widget = TimePickerInput()
        return form

    def form_valid(self, form):
        routine = form.save(commit=False)
        routine.save()
        return redirect('routine_list')


def routine_delete(request, pk):
    routine = get_object_or_404(Routine, pk=pk)
    data = dict()
    if request.method == 'POST':
        routine.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        routines = Routine.objects.all()
        data['html_routine_list'] = render_to_string('routines/includes/partial_routine_list.html', {
            'routines': routines
        })
    else:
        context = {'routine': routine}
        data['html_form'] = render_to_string('routines/includes/partial_routine_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF ROUTINE MODULE<===##########################################

# #######################################===>BEGINNING OF DISPATCH MODULE<===#####################################


class DispatchListView(ListView):
    model = Dispatch
    template_name = 'dispatch/dispatch_list.html'
    context_object_name = 'dispatch'


class DispatchCreateView(CreateView):
    model = Dispatch
    template_name = 'dispatch/dispatch_create.html'
    fields = ('to_Title', 'reference', 'address', 'from_Title', 'dispatch_date', 'note', 'postal_Attachment')

    def get_form(self):
        form = super().get_form()
        form.fields['dispatch_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        dispatch = form.save(commit=False)
        dispatch.save()
        return redirect('dispatch_list')


class DispatchUpdateView(UpdateView):
    model = Dispatch
    template_name = 'dispatch/update_dispatch.html'
    pk_url_kwarg = 'dispatch_pk'
    fields = ('to_Title', 'reference', 'address', 'from_Title', 'dispatch_date', 'note', 'postal_Attachment')

    def get_form(self):
        form = super().get_form()
        form.fields['dispatch_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        dispatch = form.save(commit=False)
        dispatch.save()
        return redirect('dispatch_list')


def dispatch_view(request, dispatch_pk):
    dispatch = get_object_or_404(Dispatch, pk=dispatch_pk)
    if request.method == 'POST':
        form = DispatchForm(request.POST, instance=dispatch)
    else:
        form = DispatchForm(instance=dispatch)
    return save_dispatch_form(request, form, 'dispatch/includes/partial_dispatch_view.html')


def save_dispatch_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            dispatchs = Dispatch.objects.all()
            data['html_dispatch_list'] = render_to_string('dispatch/includes/partial_dispatch_list.html', {
                'dispatchs': dispatchs
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def dispatch_delete(request, dispatch_pk):
    dispatch = get_object_or_404(Dispatch, pk=dispatch_pk)
    data = dict()
    if request.method == 'POST':
        dispatch.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        dispatchs = Dispatch.objects.all()
        data['html_dispatch_list'] = render_to_string('dispatch/includes/partial_dispatch_list.html', {
            'dispatchs': dispatchs
        })
    else:
        context = {'dispatch': dispatch}
        data['html_form'] = render_to_string('dispatch/includes/partial_dispatch_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF DISPATCH MODULE<===#####################################

# #######################################===>BEGINNING OF RECEIVE MODULE<===#####################################


class ReceiveListView(ListView):
    model = Receive
    template_name = 'receive/receive_list.html'
    context_object_name = 'receive'


class ReceiveCreateView(CreateView):
    model = Receive
    template_name = 'receive/receive_create.html'
    fields = ('to_Title', 'reference', 'address', 'from_Title', 'receive_date', 'note', 'postal_Attachment')

    def get_form(self):
        form = super().get_form()
        form.fields['receive_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        receive = form.save(commit=False)
        receive.save()
        return redirect('receive_list')


class ReceiveUpdateView(UpdateView):
    model = Receive
    template_name = 'receive/update_receive.html'
    pk_url_kwarg = 'receive_pk'
    fields = ('to_Title', 'reference', 'address', 'from_Title', 'receive_date', 'note', 'postal_Attachment')

    def get_form(self):
        form = super().get_form()
        form.fields['receive_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        receive = form.save(commit=False)
        receive.save()
        return redirect('receive_list')


def receive_view(request, receive_pk):
    receive = get_object_or_404(Receive, pk=receive_pk)
    if request.method == 'POST':
        form = ReceiveForm(request.POST, instance=receive)
    else:
        form = ReceiveForm(instance=receive)
    return save_receive_form(request, form, 'receive/includes/partial_receive_view.html')


def save_receive_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            receives = Receive.objects.all()
            data['html_receive_list'] = render_to_string('receive/includes/partial_receive_list.html', {
                'receives': receives
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def receive_delete(request, receive_pk):
    receive = get_object_or_404(Receive, pk=receive_pk)
    data = dict()
    if request.method == 'POST':
        receive.delete()
        data['form_is_valid'] = True
        receives = Receive.objects.all()
        data['html_receive_list'] = render_to_string('receive/includes/partial_receive_list.html', {
            'receives': receives
        })
    else:
        context = {'receive': receive}
        data['html_form'] = render_to_string('receive/includes/partial_receive_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF RECEIVE MODULE<===#####################################

# #######################################===>BEGINNING OF LEAVE MODULE<===##########################################


class LeaveListView(ListView):
    model = Leave
    template_name = 'leaves/leave_list.html'
    context_object_name = 'leaves'


def leave_create(request):
    form = LeaveForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        leave = form.save(commit=False)

        leave.applicant_type = form.cleaned_data.get('applicant_type')
        leave.leave_Type = form.cleaned_data.get('leave_Type')
        leave.total_Leave = form.cleaned_data.get('total_Leave')

        leave.save()

        leave_url = reverse('leave_list')
        return redirect(leave_url)

    context = {
        'form': form,
    }
    return render(request, 'leaves/leave_create.html', context)


class LeaveUpdateView(UpdateView):
    model = Leave
    template_name = 'leaves/update_leave.html'
    pk_url_kwarg = 'leave_pk'
    fields = ('applicant_type', 'leave_Type', 'total_Leave')

    def form_valid(self, form):
        leave = form.save(commit=False)
        leave.save()
        return redirect('leave_list')


def save_leave_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            leaves = Leave.objects.all()
            data['html_leave_list'] = render_to_string('leaves/includes/partial_leave_list.html', {
                'leaves': leaves
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def leave_delete(request, leave_pk):
    leave = get_object_or_404(Leave, pk=leave_pk)
    data = dict()
    if request.method == 'POST':
        leave.delete()
        data['form_is_valid'] = True
        leaves = Leave.objects.all()
        data['html_leave_list'] = render_to_string('leaves/includes/partial_leave_list.html', {
            'leaves': leaves
        })
    else:
        context = {'leave': leave}
        data['html_form'] = render_to_string('leaves/includes/partial_leave_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF LEAVE MODULE<===#################################################

# #######################################===>BEGINNING OF APPLICATION MODULE<===######################################


def new_application_list(request):
    new_applications = Application.objects.filter(status='New')
    return render(request, 'applications/application_list.html', {'new_applications': new_applications})


def waiting_application_list(request):
    waiting_applications = Application.objects.filter(status='Waiting')
    return render(request, 'applications/waiting_list.html', {'waiting_applications': waiting_applications})


def approved_application_list(request):
    approved_applications = Application.objects.filter(status='Approved')
    return render(request, 'applications/approved_list.html', {'approved_applications': approved_applications})


def declined_application_list(request):
    declined_applications = Application.objects.filter(status='Declined')
    return render(request, 'applications/declined_list.html', {'declined_applications': declined_applications})


# class ApplicationCreateView(CreateView):
#     model = Application
#     template_name = 'applications/application_create.html'
#     fields = ('applicant_type', 'applicant', 'leave_Type', 'application_Date', 'leave_From', 'leave_To',
#               'leave_Reason', 'leave_attachment')
#
#     def get_form(self):
#         form = super().get_form()
#         form.fields['application_Date'].widget = DatePickerInput()
#         return form
#
#     def form_valid(self, form):
#         application = form.save(commit=False)
#         application.save()
#         return redirect('application_list')

def application_create(request):
    form = ApplicationForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        application = form.save(commit=False)

        application.applicant_type = form.cleaned_data.get('applicant_type')
        application.applicant = form.cleaned_data.get('applicant')
        application.leave_Type = form.cleaned_data.get('leave_Type')
        application.application_Date = form.cleaned_data.get('application_Date')
        application.leave_From = form.cleaned_data.get('leave_From')
        application.leave_To = form.cleaned_data.get('leave_To')
        application.leave_Reason = form.cleaned_data.get('leave_Reason')
        application.leave_attachment = form.cleaned_data.get('leave_attachment')
        application.save()

        application_url = reverse('application_list')
        return redirect(application_url)

    context = {
        'form': form,
    }
    return render(request, 'applications/application_create.html', context)


class ApplicationUpdateView(UpdateView):
    model = Application
    template_name = 'applications/update_application.html'
    pk_url_kwarg = 'application_pk'
    fields = ('applicant_type', 'applicant', 'leave_Type', 'application_Date', 'leave_From', 'leave_To',
              'leave_Reason', 'leave_attachment')

    def get_form(self):
        form = super().get_form()
        form.fields['application_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        application = form.save(commit=False)
        application.save()
        return redirect('application_list')


def save_application_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            applications = Application.objects.all()
            data['html_application_list'] = render_to_string('applications/includes/partial_application_list.html', {
                'applications': applications
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def application_view(request, application_pk):
    application = get_object_or_404(Application, pk=application_pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
    else:
        form = ApplicationForm(instance=application)
    return save_application_form(request, form, 'applications/includes/partial_application_view.html')


def application_delete(request, application_pk):
    application = get_object_or_404(Application, pk=application_pk)
    data = dict()
    if request.method == 'POST':
        application.delete()
        data['form_is_valid'] = True
        applications = Application.objects.all()
        data['html_application_list'] = render_to_string('applications/includes/partial_application_list.html', {
            'applications': applications
        })
    else:
        context = {'application': application}
        data['html_form'] = render_to_string('applications/includes/partial_application_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


def application_decline(request, application_pk):
    application = get_object_or_404(Application, pk=application_pk)
    application.status = 'Declined'
    application.save()
    messages.success(request, "Application has been successfully declined!")
    return redirect('application_list')


def application_approve(request, application_pk):
    application = get_object_or_404(Application, pk=application_pk)
    application.status = 'Approved'
    application.save()
    messages.success(request, "Application has been successfully Approved!")
    return redirect('application_list')


def application_waiting(request, application_pk):
    application = get_object_or_404(Application, pk=application_pk)
    application.status = 'Waiting'
    application.save()
    messages.success(request, "Application has been successfully added to the waiting list!")
    return redirect('application_list')


# #######################################===>END OF APPLICATION MODULE<===#############################################

# #######################################===>BEGINNING OF BULK STUDENT<===###########################################


def save_bulk_student_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            bulk_students = BulkStudent.objects.all()
            data['html_bulk_student_list'] = render_to_string('bulk_students/includes/partial_bulk_student_list.html', {
                'bulk_students': bulk_students
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def bulk_student_list(request):
    bulk_students = BulkStudent.objects.all()
    return render(request, 'bulk_students/bulk_student_list.html', {'bulk_students': bulk_students})


def bulk_student_create(request):
    if request.method == 'POST':
        form = BulkStudentForm(request.POST)
    else:
        form = BulkStudentForm()
    return save_bulk_student_form(request, form, 'bulk_students/includes/partial_bulk_student_create.html')


# #######################################===>END OF BULK STUDENT MODULE<===##########################################

# #######################################===>BEGINNING OF ATTENDANCE MODULE<===#####################################


def manage_attendance(request):
    classrooms = Classroom.objects.all()
    # class_teacher_id = request.user.teacher.id
    context = {
        "classrooms": classrooms,
    }

    return render(request, 'attendance/class_list.html', context)


def mark_attendance(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    students = Student.objects.filter(classroom=classroom)
    count = students.count()
    attendance_formset = formset_factory(AttendanceForm, extra=count)
    date = datetime.today().date().strftime('%d-%m-%Y')

    if not request.user.is_authenticated:
        return redirect('attendance:login_user')

    if request.method == 'POST':
        formset = attendance_formset(request.POST)
        list = zip(students, formset)

        if formset.is_valid():
            for form, student in zip(formset, students):
                date = datetime.today()
                mark = form.cleaned_data['mark_attendance']
                print(mark)
                check_attendance = Attendance.objects.filter(classroom=classroom, date=date, student=student)
                print(check_attendance)

                if check_attendance:
                    attendance = Attendance.objects.get(classroom=classroom, date=date, student=student)
                    if attendance.status == 'Absent':
                        student.absent = student.absent - 1
                    elif attendance.status == 'Late':
                        student.late = student.late - 1
                    elif attendance.status == 'Present':
                        student.present = student.present - 1
                    attendance.status = mark
                    attendance.save()

                else:
                    attendance = Attendance()
                    attendance.classroom = classroom
                    attendance.student = student
                    attendance.date = date
                    attendance.status = mark
                    attendance.save()

                if mark == 'Absent':
                    student.absent = student.absent + 1
                if mark == 'Present':
                    student.present = student.present + 1
                if mark == 'Late':
                    student.late = student.late + 1
                student.save()

            context = {
                'students': students,
                'classroom': classroom,
            }
            # return render(request, 'attendance/profile.html', context)
            return redirect('manage_attendance')
        else:
            error = "Something went wrong"
            context = {
                'error': error,
                'formset': formset,
                'students': students,
                'classroom': classroom,
                'list': list,
                'date': date,
            }
            return render(request, 'attendance/student_list.html', context)

    else:
        list = zip(students, attendance_formset())
        context = {
            'formset': attendance_formset(),
            'students': students,
            'classroom': classroom,
            'list': list,
            'date': date,
        }

        return render(request, 'attendance/student_list.html', context)


def attendance_teacher(request):
    teachers = Teacher.objects.filter()
    count = teachers.count()
    attendance_formset = formset_factory(AttendanceForm, extra=count)
    date = datetime.today().date().strftime('%d-%m-%Y')

    if not request.user.is_authenticated:
        return redirect('attendance:login_user')

    if request.method == 'POST':
        formset = attendance_formset(request.POST)
        list = zip(teachers, formset)

        if formset.is_valid():
            for form, teacher in zip(formset, teachers):
                date = datetime.today()
                mark = form.cleaned_data['attendance_teacher']
                print(mark)
                check_attendance = TeacherAttendance.objects.filter(date=date, teacher=teacher)
                print(check_attendance)

                if check_attendance:
                    attendance = TeacherAttendance.objects.get(date=date, teacher=teacher)
                    if attendance.status == 'Absent':
                        teacher.absent = teacher.absent - 1
                    elif attendance.status == 'Late':
                        teacher.late = teacher.late - 1
                    elif attendance.status == 'Present':
                        teacher.present = teacher.present - 1
                    attendance.status = mark
                    attendance.save()

                else:
                    attendance = TeacherAttendance()
                    attendance.teacher = teacher
                    attendance.date = date
                    attendance.status = mark
                    attendance.save()

                if mark == 'Absent':
                    teacher.absent = teacher.absent + 1
                if mark == 'Present':
                    teacher.present = teacher.present + 1
                if mark == 'Late':
                    teacher.late = teacher.late + 1
                teacher.save()

            context = {
                'teachers': teachers,
            }
            # return render(request, 'attendance/profile.html', context)
            return redirect('attendance_teacher')
        else:
            error = "Something went wrong"
            context = {
                'error': error,
                'formset': formset,
                'teachers': teachers,
                'list': list,
                'date': date,
            }
            return render(request, 'attendance/teacher_list.html', context)

    else:
        list = zip(teachers, attendance_formset())
        context = {
            'formset': attendance_formset(),
            'teachers': teachers,
            'list': list,
            'date': date,
        }

        return render(request, 'attendance/teacher_list.html', context)


def attendance_employee(request):
    employees = Employee.objects.filter()
    count = employees.count()
    attendance_formset = formset_factory(AttendanceForm, extra=count)
    date = datetime.today().date().strftime('%d-%m-%Y')

    if not request.user.is_authenticated:
        return redirect('attendance:login_user')

    if request.method == 'POST':
        formset = attendance_formset(request.POST)
        list = zip(employees, formset)

        if formset.is_valid():
            for form, employee in zip(formset, employees):
                date = datetime.today()
                mark = form.cleaned_data['attendance_employee']
                print(mark)
                check_attendance = EmployeeAttendance.objects.filter(date=date, employee=employee)
                print(check_attendance)

                if check_attendance:
                    attendance = EmployeeAttendance.objects.get(date=date, employee=employee)
                    if attendance.status == 'Absent':
                        employee.absent = employee.absent - 1
                    elif attendance.status == 'Late':
                        employee.late = employee.late - 1
                    elif attendance.status == 'Present':
                        employee.present = employee.present - 1
                    attendance.status = mark
                    attendance.save()

                else:
                    attendance = EmployeeAttendance()
                    attendance.employee = employee
                    attendance.date = date
                    attendance.status = mark
                    attendance.save()

                if mark == 'Absent':
                    employee.absent = employee.absent + 1
                if mark == 'Present':
                    employee.present = employee.present + 1
                if mark == 'Late':
                    employee.late = employee.late + 1
                employee.save()

            context = {
                'employees': employees,
            }
            # return render(request, 'attendance/profile.html', context)
            return redirect('attendance_employee')
        else:
            error = "Something went wrong"
            context = {
                'error': error,
                'formset': formset,
                'employees': employees,
                'list': list,
                'date': date,
            }
            return render(request, 'attendance/employee_list.html', context)

    else:
        list = zip(employees, attendance_formset())
        context = {
            'formset': attendance_formset(),
            'employees': employees,
            'list': list,
            'date': date,
        }

        return render(request, 'attendance/employee_list.html', context)


def attendance_report(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    if request.user.is_authenticated:
        date = datetime.today().date()
        attendance = Attendance.objects.filter(date=datetime.today())
        students = Student.objects.filter(classroom=classroom)

        # For overview report
        studentMen = students.filter(user__gender='Male')
        studentFemale = students.filter(user__gender='Female')
        boys = attendance.filter(student__in=studentMen)
        girls = attendance.filter(student__in=studentFemale)
        p_boys = boys.filter(status='Present')
        p_girls = girls.filter(status='Present')
        a_boys = boys.filter(status='Absent')
        a_girls = girls.filter(status='Absent')
        l_boys = boys.filter(status='Late')
        l_girls = girls.filter(status='Late')

        # For detailed report
        boys_present = []
        girls_present = []
        boys_absent = []
        girls_absent = []
        boys_late = []
        girls_late = []
        total_present = []
        total_absent = []
        total_late = []
        student_data = []

        classrooms = Classroom.objects.all()
        for classroom in classrooms:
            st = students.filter(classroom=classroom)
            student_data.append(st)
            stMen = st.filter(user__gender='Male')
            stFemale = st.filter(user__gender='Female')
            boy = attendance.filter(student__in=stMen)
            girl = attendance.filter(student__in=stFemale)
            boys_present.append(boy.filter(status='Present').count())
            girls_present.append(girl.filter(status='Present').count())
            boys_absent.append(boy.filter(status='Absent').count())
            girls_absent.append(girl.filter(status='Absent').count())
            boys_late.append(boy.filter(status='Late').count())
            girls_late.append(girl.filter(status='Late').count())
            total_present.append(
                boy.filter(status='Present').count() + girl.filter(status='Present').count())
            total_absent.append(
                boy.filter(status='Absent').count() + girl.filter(status='Absent').count())
            total_late.append(
                boy.filter(status='Late').count() + girl.filter(status='Late').count())

        report_data = zip(classrooms,
                          boys_present,
                          boys_absent,
                          boys_late,
                          girls_present,
                          girls_absent,
                          girls_late,
                          total_present,
                          total_absent,
                          total_late,
                          student_data)

        context = {
            'date': date,
            'classroom': classroom,
            'classrooms': classrooms,
            'attendance': attendance,
            'p_boys': p_boys,
            'a_boys': a_boys,
            'l_boys': l_boys,
            'p_girls': p_girls,
            'a_girls': a_girls,
            'l_girls': l_girls,
            'report_data': report_data,
        }
        return render(request, 'attendance/student_attendance_report.html', context)
    else:
        return redirect('manage_attendance')


def export_to_csv(request, pk):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report-{}.csv"'.format(datetime.today().date())
    writer = csv.writer(response)
    writer.writerow(
        ['Class', 'Section', 'Boys(Present)', 'Boys(Absent)', 'Girls(Present)', 'Girls(Absent)', 'Total(Present)',
         'Total(Absent)'])

    # Data For Report
    classrooms = Classroom.objects.filter(pk=pk)
    attendance = Attendance.objects.filter(date=datetime.today()).filter(classroom__in=classrooms)
    students = Student.objects.filter(classroom__in=classrooms)

    # Data Writing
    for classroom in classrooms:
        row = []
        st = students.filter(classroom=classroom)
        stMen = st.filter(user__gender='Male')
        stFemale = st.filter(user__gender='Female')
        boy = attendance.filter(student__in=stMen)
        girl = attendance.filter(student__in=stFemale)
        row.append(classroom.classroom)
        row.append(classroom.classroom)
        row.append(boy.filter(status='Present').count())
        row.append(boy.filter(status='Absent').count())
        row.append(girl.filter(status='Present').count())
        row.append(girl.filter(status='Absent').count())
        row.append(boy.filter(status='Present').count() + girl.filter(status='Present').count())
        row.append(boy.filter(status='Absent').count() + girl.filter(status='Absent').count())
        writer.writerow(row)
    return response


# #######################################===>END OF ATTENDANCE MODULE<===##########################################

# #######################################===>BEGINNING OF ASSIGNMENT MODULE<===#####################################


class AssignmentListView(ListView):
    model = Assignment
    template_name = 'assignments/assignment_list.html'
    context_object_name = 'assignments'


def assignment_create(request):
    form = AssignmentForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        assignment = form.save(commit=False)

        assignment.assignment_title = form.cleaned_data.get('assignment_title')
        assignment.classroom = form.cleaned_data.get('classroom')
        assignment.subject = form.cleaned_data.get('subject')
        assignment.assignment = form.cleaned_data.get('assignment')
        assignment.note = form.cleaned_data.get('note')

        assignment.save()

        assignment_url = reverse('assignment_list')
        return redirect(assignment_url)

    context = {
        'form': form,
    }
    return render(request, 'assignments/assignment_create.html', context)


class AssignmentUpdateView(UpdateView):
    model = Assignment
    template_name = 'assignments/update_assignment.html'
    pk_url_kwarg = 'assignment_pk'
    fields = ('assignment_title', 'classroom', 'subject', 'deadline', 'assignment', 'note')

    def form_valid(self, form):
        assignment = form.save(commit=False)
        assignment.save()
        return redirect('assignment_list')


def assignment_view(request, assignment_pk):
    assignment = get_object_or_404(Assignment, pk=assignment_pk)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
    else:
        form = AssignmentForm(instance=assignment)
    return save_assignment_form(request, form, 'assignments/includes/partial_assignment_view.html')


def save_assignment_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            assignments = Assignment.objects.all()
            data['html_assignment_list'] = render_to_string('assignments/includes/partial_assignment_list.html', {
                'assignments': assignments
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def assignment_delete(request, assignment_pk):
    assignment = get_object_or_404(Assignment, pk=assignment_pk)
    data = dict()
    if request.method == 'POST':
        assignment.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        assignments = Assignment.objects.all()
        data['html_assignment_list'] = render_to_string('assignments/includes/partial_assignment_list.html', {
            'assignments': assignments
        })
    else:
        context = {'assignment': assignment}
        data['html_form'] = render_to_string('assignments/includes/partial_assignment_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF ASSIGNMENT MODULE<===##########################################

# #######################################===>BEGINNING OF MARK MODULE<===##########################################


def manage_mark(request):
    current_year = Year.objects.get(is_current_year=True)
    current_term = get_object_or_404(Term, is_current_term=True, year=current_year)
    term = Subject.objects.filter(subject_teacher__pk=request.user.id, term=current_term)
    subjects = Subject.objects.filter(subject_teacher__pk=request.user.id).filter(term=current_term)
    context = {
        "subjects": subjects,
    }

    return render(request, 'marks/sheet_marks.html', context)


def submit_mark(request, mark_pk):
    current_term = Term.objects.get(is_current_term=True)
    current_year = Year.objects.get(is_current_year=True)
    if request.method == 'GET':
        subjects = Subject.objects.filter(subject_teacher__pk=request.user.id).filter(
            term=current_term)
        year = current_year
        subject = Subject.objects.get(pk=mark_pk)
        students = TakenSubject.objects.filter(subject__subject_teacher__pk=request.user.id).filter(
            subject__id=mark_pk).filter(subject__term=current_term)
        context = {
            "year": year,
            "subjects": subjects,
            "subject": subject,
            "students": students,
        }
        return render(request, 'marks/submit_marks.html', context)

    if request.method == 'POST':
        ids = ()
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None)  # remove csrf_token
        for key in data.keys():
            ids = ids + (str(key),)  # gather all the all students id (i.e the keys) in a tuple
        for s in range(0, len(ids)):  # iterate over the list of student ids gathered above
            student = TakenSubject.objects.get(id=ids[s])
            subjects = Subject.objects.filter(classroom=student.student.classroom).filter(
                term=current_term)  # all subjects of a specific classroom in current term
            total_unit_in_term = 0
            for i in subjects:
                if i == subjects.count():
                    break
                else:
                    total_unit_in_term += int(i.subject_unit)
            score = data.getlist(ids[s])  # get list of score for current student in the loop
            bot = score[0]  # subscript the list to get the first value > bot score
            mot = score[1]  # do the same for mot score
            eot = score[2]  # do the same for eot score
            obj = TakenSubject.objects.get(pk=ids[s])  # get the current student data
            obj.bot = bot  # set current student B.O.T score
            obj.mot = mot  # set current student M.O.T score
            obj.eot = eot  # set current student E.O.T score
            obj.total = obj.get_total(bot=bot, mot=mot, eot=eot)
            obj.grade = obj.get_grade(bot=bot, mot=mot, eot=eot)
            obj.comment = obj.get_comment(obj.grade)
            obj.carry_over(obj.grade)
            obj.is_repeating(obj.grade)
            obj.save()
            gpa = obj.calculate_gpa(total_unit_in_term)
            cgpa = obj.calculate_cgpa()
            try:
                a = Result.objects.get(student=student.student, term=current_term, year=current_year,
                                       classroom=student.student.classroom)
                a.gpa = gpa
                a.cgpa = cgpa
                a.save()
            except:
                Result.objects.get_or_create(student=student.student, gpa=gpa, term=current_term,
                                             classroom=student.student.classroom)
        messages.success(request, 'Successfully Recorded! ')
        return HttpResponseRedirect(reverse_lazy('submit_mark', kwargs={'mark_pk': mark_pk}))
    return HttpResponseRedirect(reverse_lazy('submit_mark', kwargs={'mark_pk': mark_pk}))


def view_result(request):
    student = Student.objects.get(user__pk=request.user.id)
    current_term = Term.objects.get(is_current_term=True)
    subjects = TakenSubject.objects.filter(student__user__pk=request.user.id, subject__classroom=student.classroom)
    result = Result.objects.filter(student__user__pk=request.user.id)
    current_term_grades = {}

    previousCGPA = 0
    previousCLASSROOM = 0

    for i in result:
        if not i.classroom == i.student.classroom:  # TODO think n check the logic
            previousCLASSROOM = i.classroom
            try:
                a = Result.objects.get(student__user__pk=request.user.id, classroom=previousCLASSROOM, term="Second")
                previousCGPA = a.cgpa
                break
            except:
                previousCGPA = 0
        else:
            break
    context = {
        "subjects": subjects,
        "result": result,
        "student": student,
        "previousCGPA": previousCGPA,
    }

    return render(request, 'marks/view_results.html', context)


def promote(request):
    if request.method == "POST":
        value = ()
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None)  # remove csrf_token
        for val in data.values():
            value += (val,)
        subject = value[0]
        year = value[1]
        subjects = CarryOverStudent.objects.filter(subject=subject, year=year)
        all_subjects = Subject.objects.all()
        years = Year.objects.all()
        signal_template = True
        context = {
            "all_subjects": all_subjects,
            "subjects": subjects,
            "signal_template": signal_template,
            "years": years
        }
        return render(request, 'promotion/carry_over.html', context)
    else:
        all_subjects = Subject.objects.all()
        years = Year.objects.all()
        return render(request, 'promotion/carry_over.html', {"all_subjects": all_subjects, "years": years})


# #######################################===>END OF MARK MODULE<===#################################################

# #######################################===>BEGINNING OF EXAM GRADE MODULE<===#####################################


class ExamGradeListView(ListView):
    model = ExamGrade
    template_name = 'exam_grades/exam_grade_list.html'
    context_object_name = 'exam_grades'


class ExamGradeCreateView(CreateView):
    model = ExamGrade
    template_name = 'exam_grades/exam_grade_create.html'
    fields = ('exam_grade', 'grade_point', 'mark_from', 'mark_to', 'note')

    def form_valid(self, form):
        exam_grade = form.save(commit=False)
        exam_grade.save()
        return redirect('exam_grade_list')


class ExamGradeUpdateView(UpdateView):
    model = ExamGrade
    template_name = 'exam_grades/update_exam_grade.html'
    pk_url_kwarg = 'exam_grade_pk'
    fields = ('exam_grade', 'grade_point', 'mark_from', 'mark_to', 'note')

    def form_valid(self, form):
        exam_grade = form.save(commit=False)
        exam_grade.save()
        return redirect('exam_grade_list')


def save_exam_grade_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            exam_grades = ExamGrade.objects.all()
            data['html_exam_grade_list'] = render_to_string('exam_grades/includes/partial_exam_grade_list.html', {
                'exam_grades': exam_grades
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def exam_grade_delete(request, exam_grade_pk):
    exam_grade = get_object_or_404(ExamGrade, pk=exam_grade_pk)
    data = dict()
    if request.method == 'POST':
        exam_grade.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        exam_grades = ExamGrade.objects.all()
        data['html_exam_grade_list'] = render_to_string('exam_grades/includes/partial_exam_grade_list.html', {
            'exam_grades': exam_grades
        })
    else:
        context = {'exam_grade': exam_grade}
        data['html_form'] = render_to_string('exam_grades/includes/partial_exam_grade_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF EXAM GRADE MODULE<===##########################################

# ###################################===>BEGINNING OF SUBJECT REGISTRATION MODULE<===################################


# #######################################===>BEGINNING OF EXAM MODULE<===##########################################

class ExamListView(ListView):
    model = Exam
    template_name = 'exams/exam_list.html'
    context_object_name = 'exams'

    def get(self, request):
        form = ExamForm
        exams = Exam.objects.all()
        current_year = Year.objects.get(is_current_year=True)
        args = {'form': form, 'exams': exams, 'current_year': current_year}
        return render(request, self.template_name, args)


class ExamCreateView(CreateView):
    model = Exam
    template_name = 'exams/exam_create.html'
    fields = ('exam_title', 'start_date', 'note')

    def get_form(self):
        form = super().get_form()
        form.fields['start_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        exam = form.save(commit=False)
        exam.save()
        return redirect('exam_list')


class ExamUpdateView(UpdateView):
    model = Exam
    template_name = 'exams/update_exam.html'
    pk_url_kwarg = 'exam_pk'
    fields = ('exam_title', 'start_date', 'note')

    def get_form(self):
        form = super().get_form()
        form.fields['start_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        exam = form.save(commit=False)
        exam.save()
        return redirect('exam_list')


def save_exam_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            exams = Exam.objects.all()
            data['html_exam_list'] = render_to_string('exams/includes/partial_exam_list.html', {
                'exams': exams
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def exam_delete(request, exam_pk):
    exam = get_object_or_404(Exam, pk=exam_pk)
    data = dict()
    if request.method == 'POST':
        exam.delete()
        data['form_is_valid'] = True
        exams = Exam.objects.all()
        data['html_exam_list'] = render_to_string('exams/includes/partial_exam_list.html', {
            'exams': exams
        })
    else:
        context = {'exam': exam}
        data['html_form'] = render_to_string('exams/includes/partial_exam_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF EXAM MODULE<===#################################################

# #######################################===>BEGINNING OF EXAM SCHEDULE MODULE<===###################################


class ExamScheduleListView(ListView):
    model = ExamSchedule
    template_name = 'exam_schedules/exam_schedule_list.html'
    context_object_name = 'exam_schedules'


class ExamScheduleCreateView(CreateView):
    model = ExamSchedule
    template_name = 'exam_schedules/exam_schedule_create.html'
    fields = ('exam', 'classroom', 'subject', 'exam_date', 'start_time', 'end_time', 'room_no', 'note')

    def get_form(self):
        form = super().get_form()
        form.fields['exam_date'].widget = DatePickerInput()
        form.fields['start_time'].widget = TimePickerInput()
        form.fields['end_time'].widget = TimePickerInput()
        return form

    def form_valid(self, form):
        exam = form.save(commit=False)
        exam.save()
        return redirect('exam_schedule_list')


class ExamScheduleUpdateView(UpdateView):
    model = ExamSchedule
    template_name = 'exam_schedules/update_exam_schedule.html'
    pk_url_kwarg = 'exam_schedule_pk'
    fields = ('exam', 'classroom', 'subject', 'exam_date', 'start_time', 'end_time', 'room_no', 'note')

    def get_form(self):
        form = super().get_form()
        form.fields['exam_date'].widget = DatePickerInput()
        form.fields['start_time'].widget = TimePickerInput()
        form.fields['end_time'].widget = TimePickerInput()
        return form

    def form_valid(self, form):
        exam_schedule = form.save(commit=False)
        exam_schedule.save()
        return redirect('exam_schedule_list')


def save_exam_schedule_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            exam_schedules = ExamSchedule.objects.all()
            data['html_exam_schedule_list'] = render_to_string(
                'exam_schedules/includes/partial_exam_schedule_list.html', {
                    'exam_schedules': exam_schedules
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def exam_schedule_delete(request, exam_schedule_pk):
    exam_schedule = get_object_or_404(ExamSchedule, pk=exam_schedule_pk)
    data = dict()
    if request.method == 'POST':
        exam_schedule.delete()
        data['form_is_valid'] = True
        exam_schedules = ExamSchedule.objects.all()
        data['html_exam_schedule_list'] = render_to_string('exam_schedules/includes/partial_exam_schedule_list.html', {
            'exam_schedules': exam_schedules
        })
    else:
        context = {'exam_schedule': exam_schedule}
        data['html_form'] = render_to_string('exam_schedules/includes/partial_exam_schedule_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF EXAM SCHEDULE MODULE<===##########################################

# #######################################===>BEGINNING OF EXAM SUGGESTION MODULE<===##################################


class ExamSuggestionListView(ListView):
    model = ExamSuggestion
    template_name = 'exam_suggestions/exam_suggestion_list.html'
    context_object_name = 'exam_suggestions'


class ExamSuggestionCreateView(CreateView):
    model = ExamSuggestion
    template_name = 'exam_suggestions/exam_suggestion_create.html'
    fields = ('suggestion_title', 'exam', 'classroom', 'subject', 'suggestion', 'note')

    def form_valid(self, form):
        exam_suggestion = form.save(commit=False)
        exam_suggestion.save()
        return redirect('exam_suggestion_list')


class ExamSuggestionUpdateView(UpdateView):
    model = ExamSuggestion
    template_name = 'exam_suggestions/update_exam_suggestion.html'
    pk_url_kwarg = 'exam_suggestion_pk'
    fields = ('suggestion_title', 'exam', 'classroom', 'subject', 'suggestion', 'note')

    def form_valid(self, form):
        exam_suggestion = form.save(commit=False)
        exam_suggestion.save()
        return redirect('exam_suggestion_list')


def save_exam_suggestion_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            exam_suggestions = ExamSuggestion.objects.all()
            data['html_exam_suggestion_list'] = render_to_string(
                'exam_suggestions/includes/partial_exam_suggestion_list.html', {
                    'exam_suggestions': exam_suggestions
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def exam_suggestion_delete(request, exam_suggestion_pk):
    exam_suggestion = get_object_or_404(ExamSuggestion, pk=exam_suggestion_pk)
    data = dict()
    if request.method == 'POST':
        exam_suggestion.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        exam_suggestions = ExamSuggestion.objects.all()
        data['html_exam_suggestion_list'] = render_to_string(
            'exam_suggestions/includes/partial_exam_suggestion_list.html', {
                'exam_suggestions': exam_suggestions
            })
    else:
        context = {'exam_suggestion': exam_suggestion}
        data['html_form'] = render_to_string('exam_suggestions/includes/partial_exam_suggestion_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF EXAM SUGGESTION MODULE<===#########################################

# #######################################===>BEGINNING OF CERTIFICATE MODULE<===#######################################


class CertificateListView(ListView):
    model = CertificateType
    template_name = 'certificates/certificate_list.html'
    context_object_name = 'certificates'


class CertificateCreateView(CreateView):
    model = CertificateType
    template_name = 'certificates/certificate_create.html'
    fields = ('certificate_name', 'school_name', 'certificate_text', 'footer_left_text', 'footer_middle_text',
              'footer_right_text', 'background')

    def form_valid(self, form):
        certificate = form.save(commit=False)
        certificate.save()
        return redirect('certificate_list')


class CertificateUpdateView(UpdateView):
    model = CertificateType
    template_name = 'certificates/update_certificate.html'
    pk_url_kwarg = 'certificate_pk'
    fields = ('certificate_name', 'school_name', 'certificate_text', 'footer_left_text', 'footer_middle_text',
              'footer_right_text', 'background')

    def form_valid(self, form):
        certificate = form.save(commit=False)
        certificate.save()
        return redirect('certificate_list')


def save_certificate_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            certificates = CertificateType.objects.all()
            data['html_certificate_list'] = render_to_string('certificates/includes/partial_certificate_list.html', {
                'certificates': certificates
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def certificate_view(request, certificate_pk):
    certificate = get_object_or_404(CertificateType, pk=certificate_pk)
    if request.method == 'POST':
        form = CertificateForm(request.POST, instance=certificate)
    else:
        form = CertificateForm(instance=certificate)
    context = {'form': form}
    return render(request, 'certificates/certificate_view.html', context)


def certificate_delete(request, certificate_pk):
    certificate = get_object_or_404(CertificateType, pk=certificate_pk)
    data = dict()
    if request.method == 'POST':
        certificate.delete()
        data['form_is_valid'] = True
        certificates = CertificateType.objects.all()
        data['html_certificate_list'] = render_to_string('certificates/includes/partial_certificate_list.html', {
            'certificates': certificates
        })
    else:
        context = {'certificate': certificate}
        data['html_form'] = render_to_string('certificates/includes/partial_certificate_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF CERTIFICATE MODULE<===#####################################

# #######################################===>BEGINNING OF BOOK MODULE<===#####################################


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'


class BookCreateView(CreateView):
    model = Book
    template_name = 'books/book_create.html'
    fields = ('book_title', 'book_ID', 'ISBN_no', 'edition', 'author', 'language', 'price', 'quantity',
              'almira_no', 'book_cover')

    def form_valid(self, form):
        book = form.save(commit=False)
        book.save()
        return redirect('book_list')


class BookUpdateView(UpdateView):
    model = Book
    template_name = 'books/update_book.html'
    pk_url_kwarg = 'book_pk'
    fields = ('book_title', 'book_ID', 'ISBN_no', 'edition', 'author', 'language', 'price', 'quantity',
              'almira_no', 'book_cover')

    def form_valid(self, form):
        book = form.save(commit=False)
        book.save()
        return redirect('book_list')


def save_book_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = Book.objects.all()
            data['html_book_list'] = render_to_string('books/includes/partial_book_list.html', {
                'books': books
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def book_view(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
    else:
        form = BookForm(instance=book)
    return save_book_form(request, form, 'books/includes/partial_book_view.html')


def book_delete(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    data = dict()
    if request.method == 'POST':
        book.delete()
        data['form_is_valid'] = True
        books = Book.objects.all()
        data['html_book_list'] = render_to_string('books/includes/partial_book_list.html', {
            'books': books
        })
    else:
        context = {'book': book}
        data['html_form'] = render_to_string('books/includes/partial_book_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF BOOK MODULE<===##################################################


# #######################################===>BEGINNING OF PURPOSE MODULE<===#####################################


class PurposeListView(ListView):
    model = Purpose
    template_name = 'purposes/purpose_list.html'
    context_object_name = 'purposes'


class PurposeCreateView(CreateView):
    model = Purpose
    template_name = 'purposes/purpose_create.html'
    fields = ['visitor_purpose']

    def form_valid(self, form):
        purpose = form.save(commit=False)
        purpose.save()
        return redirect('purpose_list')


class PurposeUpdateView(UpdateView):
    model = Purpose
    template_name = 'purposes/update_purpose.html'
    pk_url_kwarg = 'purpose_pk'
    fields = ('visitor_purpose')

    def form_valid(self, form):
        purpose = form.save(commit=False)
        purpose.save()
        return redirect('purpose_list')


def save_purpose_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            purposes = Purpose.objects.all()
            data['html_purpose_list'] = render_to_string('purposes/includes/partial_purpose_list.html', {
                'purposes': purposes
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def purpose_delete(request, purpose_pk):
    purpose = get_object_or_404(Purpose, pk=purpose_pk)
    data = dict()
    if request.method == 'POST':
        purpose.delete()
        data['form_is_valid'] = True
        purposes = Purpose.objects.all()
        data['html_purpose_list'] = render_to_string('purposes/includes/partial_purpose_list.html', {
            'purposes': purposes
        })
    else:
        context = {'purpose': purpose}
        data['html_form'] = render_to_string('purposes/includes/partial_purpose_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF PURPOSE MODULE<===##################################################

# #######################################===>BEGINNING OF E-PURPOSE MODULE<===#####################################


class EBookListView(ListView):
    model = EBook
    template_name = 'ebooks/ebook_list.html'
    context_object_name = 'ebooks'


class EBookCreateView(CreateView):
    model = EBook
    template_name = 'ebooks/ebook_create.html'
    fields = ('classroom', 'subject', 'EBook_title', 'edition', 'author', 'language', 'cover_image', 'e_book')

    def form_valid(self, form):
        ebook = form.save(commit=False)
        ebook.save()
        return redirect('ebook_list')


class EBookUpdateView(UpdateView):
    model = EBook
    template_name = 'ebooks/update_ebook.html'
    pk_url_kwarg = 'ebook_pk'
    fields = ('classroom', 'subject', 'EBook_title', 'edition', 'author', 'language', 'cover_image', 'e_book')

    def form_valid(self, form):
        eBook = form.save(commit=False)
        eBook.save()
        return redirect('ebook_list')


def save_ebook_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            eBooks = EBook.objects.all()
            data['html_ebook_list'] = render_to_string('ebooks/includes/partial_ebook_list.html', {
                'eBooks': eBooks
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def ebook_view(request, ebook_pk):
    eBook = get_object_or_404(EBook, pk=ebook_pk)
    if request.method == 'POST':
        form = EBookForm(request.POST, instance=eBook)
    else:
        form = EBookForm(instance=eBook)
    return save_ebook_form(request, form, 'eBooks/includes/partial_eBook_view.html')


def ebook_delete(request, ebook_pk):
    ebook = get_object_or_404(EBook, pk=ebook_pk)
    data = dict()
    if request.method == 'POST':
        ebook.delete()
        data['form_is_valid'] = True
        ebooks = EBook.objects.all()
        data['html_ebook_list'] = render_to_string('ebooks/includes/partial_ebook_list.html', {
            'ebooks': ebooks
        })
    else:
        context = {'ebook': ebook}
        data['html_form'] = render_to_string('ebooks/includes/partial_ebook_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF E-BOOK MODULE<===##################################################

# #######################################===>BEGINNING OF LIBRARY MEMBER MODULE<===###################################


class LibraryMemberListView(ListView):
    model = LibraryMember
    template_name = 'library_members/library_member_list.html'
    context_object_name = 'library_members'


class LibraryMemberCreateView(CreateView):
    model = LibraryMember
    template_name = 'library_members/library_member_create.html'
    fields = ('photo', 'library_ID', 'name', 'classroom', 'section', 'roll_no')

    def form_valid(self, form):
        library_member = form.save(commit=False)
        library_member.save()
        return redirect('library_member_list')


class LibraryMemberUpdateView(UpdateView):
    model = LibraryMember
    template_name = 'library_members/update_library_member.html'
    pk_url_kwarg = 'library_member_pk'
    fields = ('photo', 'library_ID', 'name', 'classroom', 'section', 'roll_no')

    def form_valid(self, form):
        library_member = form.save(commit=False)
        library_member.save()
        return redirect('library_member_list')


def save_library_member_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            library_members = LibraryMember.objects.all()
            data['html_library_member_list'] = render_to_string(
                'library_members/includes/partial_library_member_list.html', {
                    'library_members': library_members
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def library_member_delete(request, library_member_pk):
    library_member = get_object_or_404(LibraryMember, pk=library_member_pk)
    data = dict()
    if request.method == 'POST':
        library_member.delete()
        data['form_is_valid'] = True
        library_members = LibraryMember.objects.all()
        data['html_library_member_list'] = render_to_string('library_members/includes/partial_library_member_list.html',
                                                            {
                                                                'library_members': library_members
                                                            })
    else:
        context = {'library_member': library_member}
        data['html_form'] = render_to_string('library_members/includes/partial_library_member_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF LIBRARY MEMBER MODULE<===#######################################

# #######################################===>BEGINNING OF ISSUE MODULE<===##########################################


class IssueListView(ListView):
    model = Issue
    template_name = 'issues/issue_list.html'
    context_object_name = 'issues'


class IssueCreateView(CreateView):
    model = Issue
    template_name = 'issues/issue_create.html'
    fields = (
        'select_book', 'library_member', 'ISBN_no', 'edition', 'author', 'language', 'price', 'quantity',
        'almira_no', 'book_cover', 'return_date')

    def get_form(self):
        form = super().get_form()
        form.fields['return_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        issue = form.save(commit=False)
        issue.save()
        return redirect('issue_list')


class IssueUpdateView(UpdateView):
    model = Issue
    template_name = 'issues/update_issue.html'
    pk_url_kwarg = 'issue_pk'
    fields = (
        'select_book', 'library_member', 'ISBN_no', 'edition', 'author', 'language', 'price', 'quantity',
        'almira_no', 'book_cover', 'return_date')

    def get_form(self):
        form = super().get_form()
        form.fields['return_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        issue = form.save(commit=False)
        issue.save()
        return redirect('issue_list')


def save_issue_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            issues = Issue.objects.all()
            data['html_issue_list'] = render_to_string('issues/includes/partial_issue_list.html', {
                'issues': issues
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def issue_delete(request, issue_pk):
    issue = get_object_or_404(Issue, pk=issue_pk)
    data = dict()
    if request.method == 'POST':
        issue.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        issues = Issue.objects.all()
        data['html_issue_list'] = render_to_string('issues/includes/partial_issue_list.html', {
            'issues': issues
        })
    else:
        context = {'issue': issue}
        data['html_form'] = render_to_string('issues/includes/partial_issue_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF ISSUE MODULE<===#################################################

# #######################################===>BEGINNING OF VEHICLE MODULE<===##########################################

class VehicleListView(ListView):
    model = Vehicle
    template_name = 'vehicles/vehicle_list.html'
    context_object_name = 'vehicles'


class VehicleCreateView(CreateView):
    model = Vehicle
    template_name = 'vehicles/vehicle_create.html'
    fields = ('vehicle_number', 'vehicle_model', 'driver', 'vehicle_licence', 'vehicle_contact', 'note')

    def form_valid(self, form):
        vehicle = form.save(commit=False)
        vehicle.save()
        return redirect('vehicle_list')


class VehicleUpdateView(UpdateView):
    model = Vehicle
    template_name = 'vehicles/update_vehicle.html'
    pk_url_kwarg = 'vehicle_pk'
    fields = ('vehicle_number', 'vehicle_model', 'driver', 'vehicle_licence', 'vehicle_contact', 'note')

    def form_valid(self, form):
        vehicle = form.save(commit=False)
        vehicle.save()
        return redirect('vehicle_list')


def save_vehicle_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            vehicles = Vehicle.objects.all()
            data['html_vehicle_list'] = render_to_string('vehicles/includes/partial_vehicle_list.html', {
                'vehicles': vehicles
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def vehicle_view(request, vehicle_pk):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
    else:
        form = VehicleForm(instance=vehicle)
    return save_vehicle_form(request, form, 'vehicles/includes/partial_vehicle_view.html')


def vehicle_delete(request, vehicle_pk):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_pk)
    data = dict()
    if request.method == 'POST':
        vehicle.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        vehicles = Vehicle.objects.all()
        data['html_vehicle_list'] = render_to_string('vehicles/includes/partial_vehicle_list.html', {
            'vehicles': vehicles
        })
    else:
        context = {'vehicle': vehicle}
        data['html_form'] = render_to_string('vehicles/includes/partial_vehicle_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF VEHICLE MODULE<===#################################################

# #######################################===>BEGINNING OF ROUTE MODULE<===##########################################


class RouteListView(ListView):
    model = Route
    template_name = 'routes/route_list.html'
    context_object_name = 'routes'


class RouteCreateView(CreateView):
    model = Route
    template_name = 'routes/route_create.html'
    fields = ('route_title', 'route_start', 'route_end', 'vehicle_for_route', 'stop_name', 'stop_km',
              'stop_fare', 'note')

    def form_valid(self, form):
        route = form.save(commit=False)
        route.save()
        return redirect('route_list')


class RouteUpdateView(UpdateView):
    model = Route
    template_name = 'routes/update_route.html'
    pk_url_kwarg = 'route_pk'
    fields = ('route_title', 'route_start', 'route_end', 'vehicle_for_route', 'stop_name', 'stop_km',
              'stop_fare', 'note')

    def form_valid(self, form):
        route = form.save(commit=False)
        route.save()
        return redirect('route_list')


def save_route_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            routes = Route.objects.all()
            data['html_route_list'] = render_to_string('routes/includes/partial_route_list.html', {
                'routes': routes
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def route_view(request, route_pk):
    route = get_object_or_404(Route, pk=route_pk)
    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route)
    else:
        form = RouteForm(instance=route)
    return save_vehicle_form(request, form, 'routes/includes/partial_route_view.html')


def route_delete(request, route_pk):
    route = get_object_or_404(Route, pk=route_pk)
    data = dict()
    if request.method == 'POST':
        route.delete()
        data['form_is_valid'] = True
        routes = Route.objects.all()
        data['html_route_list'] = render_to_string('routes/includes/partial_route_list.html', {
            'routes': routes
        })
    else:
        context = {'route': route}
        data['html_form'] = render_to_string('routes/includes/partial_route_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF ROUTE MODULE<===#################################################

# ###################################===>BEGINNING OF TRANSPORT MEMBER MODULE<===#####################################


class TransportMemberListView(ListView):
    model = TransportMember
    template_name = 'transport_members/transport_member_list.html'
    context_object_name = 'transport_members'


class TransportMemberCreateView(CreateView):
    model = TransportMember
    template_name = 'transport_members/transport_member_create.html'
    fields = ('photo', 'name', 'classroom', 'section', 'roll_no', 'transport_route_name', 'stop_Name',
              'stop_KM', 'stop_Fare')

    def form_valid(self, form):
        transport_member = form.save(commit=False)
        transport_member.save()
        return redirect('transport_member_list')


class TransportMemberUpdateView(UpdateView):
    model = TransportMember
    template_name = 'transport_members/update_transport_member.html'
    pk_url_kwarg = 'transport_member_pk'
    fields = ('photo', 'name', 'classroom', 'section', 'roll_no', 'transport_route_name', 'stop_Name',
              'stop_KM', 'stop_Fare')

    def form_valid(self, form):
        transport_member = form.save(commit=False)
        transport_member.save()
        return redirect('transport_member_list')


def save_transport_member_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            transport_members = TransportMember.objects.all()
            data['html_transport_member_list'] = render_to_string(
                'transport_members/includes/partial_transport_member_list.html', {
                    'transport_members': transport_members
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def transport_member_delete(request, pk):
    transport_member = get_object_or_404(TransportMember, pk=pk)
    data = dict()
    if request.method == 'POST':
        transport_member.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        transport_members = TransportMember.objects.all()
        data['html_transport_member_list'] = render_to_string(
            'transport_members/includes/partial_transport_member_list.html', {
                'transport_members': transport_members
            })
    else:
        context = {'transport_member': transport_member}
        data['html_form'] = render_to_string('transport_members/includes/partial_transport_member_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF TRANSPORT MEMBER MODULE<===######################################

# ###################################===>BEGINNING OF HOSTEL MODULE<===##############################################


class HostelListView(ListView):
    model = Hostel
    template_name = 'hostels/hostel_list.html'
    context_object_name = 'hostels'


class HostelCreateView(CreateView):
    model = Hostel
    template_name = 'hostels/hostel_create.html'
    fields = ('hostel_name', 'hostel_type', 'address', 'note')

    def form_valid(self, form):
        hostel = form.save(commit=False)
        hostel.save()
        return redirect('hostel_list')


class HostelUpdateView(UpdateView):
    model = Hostel
    template_name = 'hostels/update_hostel.html'
    pk_url_kwarg = 'hostel_pk'
    fields = ('hostel_name', 'hostel_type', 'address', 'note')

    def form_valid(self, form):
        hostel = form.save(commit=False)
        hostel.save()
        return redirect('hostel_list')


def save_hostel_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            hostels = Hostel.objects.all()
            data['html_hostel_list'] = render_to_string('hostels/includes/partial_hostel_list.html', {
                'hostels': hostels
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def hostel_view(request, hostel_pk):
    hostel = get_object_or_404(Hostel, pk=hostel_pk)
    if request.method == 'POST':
        form = HostelForm(request.POST, instance=hostel)
    else:
        form = HostelForm(instance=hostel)
    return save_vehicle_form(request, form, 'hostels/includes/partial_hostel_view.html')


def hostel_delete(request, hostel_pk):
    hostel = get_object_or_404(Hostel, pk=hostel_pk)
    data = dict()
    if request.method == 'POST':
        hostel.delete()
        data['form_is_valid'] = True
        hostels = Hostel.objects.all()
        data['html_hostel_list'] = render_to_string('hostels/includes/partial_hostel_list.html', {
            'hostels': hostels
        })
    else:
        context = {'hostel': hostel}
        data['html_form'] = render_to_string('hostels/includes/partial_hostel_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF HOSTEL MODULE<===#############################################

# ###################################===>BEGINNING OF ROOM MODULE<===##############################################

class RoomListView(ListView):
    model = Room
    template_name = 'rooms/room_list.html'
    context_object_name = 'rooms'


class RoomCreateView(CreateView):
    model = Room
    template_name = 'rooms/room_create.html'
    fields = ('room_no', 'room_type', 'seat_total', 'hostel', 'cost_per_seat', 'note')

    def form_valid(self, form):
        room = form.save(commit=False)
        room.save()
        return redirect('room_list')


class RoomUpdateView(UpdateView):
    model = Room
    template_name = 'rooms/update_room.html'
    pk_url_kwarg = 'room_pk'
    fields = ('room_no', 'room_type', 'seat_total', 'hostel', 'cost_per_seat', 'note')

    def form_valid(self, form):
        room = form.save(commit=False)
        room.save()
        return redirect('room_list')


def save_room_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            rooms = Room.objects.all()
            data['html_room_list'] = render_to_string('rooms/includes/partial_room_list.html', {
                'rooms': rooms
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def room_view(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
    else:
        form = RoomForm(instance=room)
    return save_vehicle_form(request, form, 'rooms/includes/partial_room_view.html')


def room_delete(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)
    data = dict()
    if request.method == 'POST':
        room.delete()
        data['form_is_valid'] = True
        rooms = Room.objects.all()
        data['html_room_list'] = render_to_string('rooms/includes/partial_room_list.html', {
            'rooms': rooms
        })
    else:
        context = {'room': room}
        data['html_form'] = render_to_string('rooms/includes/partial_room_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF ROOM MODULE<===################################################

# ###################################===>BEGINNING OF HOSTEL MEMBER MODULE<===#####################################


class HostelMemberListView(ListView):
    model = HostelMember
    template_name = 'hostel_members/hostel_member_list.html'
    context_object_name = 'hostel_members'


class HostelMemberCreateView(CreateView):
    model = HostelMember
    template_name = 'hostel_members/hostel_member_create.html'
    fields = ('photo', 'name', 'classroom', 'section', 'roll_no', 'hostel_name', 'room_no',
              'room_type')

    def form_valid(self, form):
        hostel_member = form.save(commit=False)
        hostel_member.save()
        return redirect('hostel_member_list')


class HostelMemberUpdateView(UpdateView):
    model = HostelMember
    template_name = 'hostel_members/update_hostel_member.html'
    pk_url_kwarg = 'member_pk'
    fields = ('photo', 'name', 'classroom', 'section', 'roll_no', 'hostel_name', 'room_no', 'room_type')

    def form_valid(self, form):
        hostel_member = form.save(commit=False)
        hostel_member.save()
        return redirect('hostel_member_list')


def save_hostel_member_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            hostel_members = HostelMember.objects.all()
            data['html_hostel_member_list'] = render_to_string(
                'hostel_members/includes/partial_hostel_member_list.html', {
                    'hostel_members': hostel_members
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def hostel_member_delete(request, member_pk):
    hostel_member = get_object_or_404(HostelMember, pk=member_pk)
    data = dict()
    if request.method == 'POST':
        hostel_member.delete()
        data['form_is_valid'] = True
        hostel_members = HostelMember.objects.all()
        data['html_hostel_member_list'] = render_to_string(
            'hostel_members/includes/partial_hostel_member_list.html', {
                'hostel_members': hostel_members
            })
    else:
        context = {'hostel_member': hostel_member}
        data['html_form'] = render_to_string('hostel_members/includes/partial_hostel_member_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF HOSTEL MEMBER MODULE<===##########################################

# ###################################===>BEGINNING OF EMAIL MODULE<===###############################################


class EmailListView(ListView):
    model = Email
    template_name = 'emails/email_list.html'
    context_object_name = 'emails'


class EmailCreateView(CreateView):
    model = Email
    template_name = 'emails/email_create.html'
    fields = ('school_name', 'receiver_type', 'receiver', 'subject', 'email_body', 'attachment')

    def form_valid(self, form):
        email = form.save(commit=False)
        email.save()
        return redirect('email_list')


def save_email_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            emails = Email.objects.all()
            data['html_email_list'] = render_to_string('emails/includes/partial_email_list.html', {
                'emails': emails
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def email_view(request, email_pk):
    email = get_object_or_404(Email, pk=email_pk)
    if request.method == 'POST':
        form = EmailForm(request.POST, instance=email)
    else:
        form = EmailForm(instance=email)
    return save_vehicle_form(request, form, 'emails/includes/partial_email_view.html')


def email_delete(request, email_pk):
    email = get_object_or_404(Email, pk=email_pk)
    data = dict()
    if request.method == 'POST':
        email.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        emails = Email.objects.all()
        data['html_email_list'] = render_to_string('emails/includes/partial_email_list.html', {
            'emails': emails
        })
    else:
        context = {'email': email}
        data['html_form'] = render_to_string('emails/includes/partial_email_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF EMAIL MODULE<===##########################################

# ###################################===>BEGINNING OF SMS MODULE<===###############################################


class SMSListView(ListView):
    model = SMS
    template_name = 'sms/sms_list.html'
    context_object_name = 'sms'


class SMSCreateView(CreateView):
    model = SMS
    template_name = 'sms/sms_create.html'
    fields = ('receiver_type', 'receiver', 'SMS', 'gateway')

    def form_valid(self, form):
        sms = form.save(commit=False)
        sms.save()
        return redirect('sms_list')


def save_sms_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            smss = SMS.objects.all()
            data['html_sms_list'] = render_to_string('sms/includes/partial_sms_list.html', {
                'sms': smss
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def sms_view(request, SMS_pk):
    sms = get_object_or_404(SMS, pk=SMS_pk)
    if request.method == 'POST':
        form = SMSForm(request.POST, instance=sms)
    else:
        form = SMSForm(instance=sms)
    return save_vehicle_form(request, form, 'sms/includes/partial_sms_view.html')


def sms_delete(request, SMS_pk):
    sms = get_object_or_404(SMS, pk=SMS_pk)
    data = dict()
    if request.method == 'POST':
        sms.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        smss = SMS.objects.all()
        data['html_sms_list'] = render_to_string('sms/includes/partial_sms_list.html', {
            'sms': smss
        })
    else:
        context = {'sms': sms}
        data['html_form'] = render_to_string('sms/includes/partial_sms_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF SMS MODULE<===##################################################

# ###################################===>BEGINNING OF MESSAGE MODULE<===##############################################

# class MessageListView(ListView):
#     model = Message
#     template_name = 'messages/message_list.html'
#     context_object_name = 'messages'
#
#
# class MessageCreateView(CreateView):
#     model = Message
#     template_name = 'messages/message_create.html'
#     fields = ('receiver_type', 'receiver', 'subject', 'message')
#
#     def form_valid(self, form):
#         message = form.save(commit=False)
#         message.save()
#         return redirect('message_inbox')
#
#
# class MessageUpdateView(UpdateView):
#     model = Message
#     template_name = 'messages/update_message.html'
#     pk_url_kwarg = 'message_pk'
#     fields = ('receiver_type', 'receiver', 'subject', 'message')
#
#     def form_valid(self, form):
#         message = form.save(commit=False)
#         message.save()
#         return redirect('message_list')
#
#
# def save_message_form(request, form, template_name):
#     data = dict()
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             data['form_is_valid'] = True
#             messages = Message.objects.all()
#             data['html_message_list'] = render_to_string('messages/includes/partial_message_list.html', {
#                 'messages': messages
#             })
#         else:
#             data['form_is_valid'] = False
#     context = {'form': form}
#     data['html_form'] = render_to_string(template_name, context, request=request)
#     return JsonResponse(data)
#
#
# def message_view(request, message_pk):
#     message = get_object_or_404(Message, pk=message_pk)
#     if request.method == 'POST':
#         form = MessageForm(request.POST, instance=message)
#     else:
#         form = MessageForm(instance=message)
#     return save_vehicle_form(request, form, 'messages/includes/partial_message_view.html')
#
#
# def message_delete(request, message_pk):
#     message = get_object_or_404(Message, pk=message_pk)
#     data = dict()
#     if request.method == 'POST':
#         message.delete()
#         data['form_is_valid'] = True
#         messages = Message.objects.all()
#         data['html_message_list'] = render_to_string('messages/includes/partial_message_list.html', {
#             'messages': messages
#         })
#     else:
#         context = {'message': message}
#         data['html_form'] = render_to_string('messages/includes/partial_message_delete.html',
#                                              context,
#                                              request=request,
#                                              )
#     return JsonResponse(data)


class MessagesListView(LoginRequiredMixin, ListView):
    """CBV to render the inbox, showing by default the most recent
    conversation as the active one.
    """
    model = Message
    paginate_by = 50
    template_name = "messages/message_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['users_list'] = get_user_model().objects.filter(
            is_active=True).exclude(
            username=self.request.user)
        # .order_by('username')
        last_conversation = Message.objects.all()
        context['active'] = last_conversation
        return context

    def get_queryset(self):
        active_user = Message.objects.all()
        return Message.objects.all()


class ConversationListView(MessagesListView):
    """CBV to render the inbox, showing an specific conversation with a given
    user, who requires to be active too."""

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active'] = self.kwargs["username"]
        return context

    def get_queryset(self):
        active_user = get_user_model().objects.get(
            username=self.kwargs["username"])
        return Message.objects.get_conversation(active_user, self.request.user)


@login_required
@ajax_required
@require_http_methods(["POST"])
def send_message(request):
    """AJAX Functional view to recieve just the minimum information, process
    and create the new message and return the new data to be attached to the
    conversation stream."""
    sender = request.user
    recipient_username = request.POST.get('to')
    recipient = get_user_model().objects.get(username=recipient_username)
    message = request.POST.get('message')
    if len(message.strip()) == 0:
        return HttpResponse()

    if sender != recipient:
        msg = Message.send_message(sender, recipient, message)
        return render(request, 'messages/single_message.html',
                      {'message': msg})

    return HttpResponse()


@login_required
@ajax_required
@require_http_methods(["GET"])
def receive_message(request):
    """Simple AJAX functional view to return a rendered single message on the
    receiver side providing realtime connections."""
    message_id = request.GET.get('message_id')
    message = Message.objects.get(pk=message_id)
    return render(request,
                  'messages/single_message.html', {'message': message})


# #######################################===>END OF MESSAGE MODULE<===################################################

# ###################################===>BEGINNING OF NOTICE MODULE<===###############################################


class NoticeListView(ListView):
    model = Notice
    template_name = 'notices/notice_list.html'
    context_object_name = 'notices'


class NoticeCreateView(CreateView):
    model = Notice
    template_name = 'notices/notice_create.html'
    fields = ('notice_title', 'date', 'notice_for', 'notice', 'Is_View_on_Web')

    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        notice = form.save(commit=False)
        notice.save()
        return redirect('notice_list')


class NoticeUpdateView(UpdateView):
    model = Notice
    template_name = 'notices/update_notice.html'
    pk_url_kwarg = 'notice_pk'
    fields = ('notice_title', 'date', 'notice_for', 'notice', 'Is_View_on_Web')

    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        notice = form.save(commit=False)
        notice.save()
        return redirect('notice_list')


def save_notice_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            notices = Notice.objects.all()
            data['html_notice_list'] = render_to_string('notices/includes/partial_notice_list.html', {
                'notices': notices
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def notice_view(request, notice_pk):
    notice = get_object_or_404(Notice, pk=notice_pk)
    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
    else:
        form = NoticeForm(instance=notice)
    return save_vehicle_form(request, form, 'notices/includes/partial_notice_view.html')


def notice_delete(request, notice_pk):
    notice = get_object_or_404(Notice, pk=notice_pk)
    data = dict()
    if request.method == 'POST':
        notice.delete()
        data['form_is_valid'] = True
        notices = Notice.objects.all()
        data['html_notice_list'] = render_to_string('notices/includes/partial_notice_list.html', {
            'notices': notices
        })
    else:
        context = {'notice': notice}
        data['html_form'] = render_to_string('notices/includes/partial_notice_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF NOTICE MODULE<===##################################################

# ###################################===>BEGINNING OF NEWS MODULE<===###############################################


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'


class NewsCreateView(CreateView):
    model = News
    template_name = 'news/news_create.html'
    fields = ('news_title', 'date', 'image', 'news', 'Is_View_on_Web')

    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        news = form.save(commit=False)
        news.save()
        return redirect('news_list')


class NewsUpdateView(UpdateView):
    model = News
    template_name = 'news/update_news.html'
    pk_url_kwarg = 'news_pk'
    fields = ('news_title', 'date', 'image', 'news', 'Is_View_on_Web')

    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        news = form.save(commit=False)
        news.save()
        return redirect('news_list')


def save_news_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            newss = News.objects.all()
            data['html_news_list'] = render_to_string('news/includes/partial_news_list.html', {
                'news': newss
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def news_view(request, news_pk):
    news = get_object_or_404(News, pk=news_pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
    else:
        form = NewsForm(instance=news)
    return save_vehicle_form(request, form, 'news/includes/partial_news_view.html')


def news_delete(request, news_pk):
    news = get_object_or_404(News, pk=news_pk)
    data = dict()
    if request.method == 'POST':
        news.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        news = News.objects.all()
        data['html_news_list'] = render_to_string('news/includes/partial_news_list.html', {
            'news': news
        })
    else:
        context = {'news': news}
        data['html_form'] = render_to_string('news/includes/partial_news_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF NEWS MODULE<===##################################################

# ###################################===>BEGINNING OF HOLIDAY MODULE<===###############################################


class HolidayListView(ListView):
    model = Holiday
    template_name = 'holidays/holiday_list.html'
    context_object_name = 'holidays'


class HolidayCreateView(CreateView):
    model = Holiday
    template_name = 'holidays/holiday_create.html'
    fields = ('holiday_title', 'from_date', 'to_date', 'note', 'Is_View_on_Web')

    def get_form(self):
        form = super().get_form()
        form.fields['from_date'].widget = DatePickerInput()
        form.fields['to_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        holiday = form.save(commit=False)
        holiday.save()
        return redirect('holiday_list')


class HolidayUpdateView(UpdateView):
    model = Holiday
    template_name = 'holidays/update_holiday.html'
    pk_url_kwarg = 'holiday_pk'
    fields = ('holiday_title', 'from_date', 'to_date', 'note', 'Is_View_on_Web')

    def get_form(self):
        form = super().get_form()
        form.fields['from_date'].widget = DatePickerInput()
        form.fields['to_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        holiday = form.save(commit=False)
        holiday.save()
        return redirect('holiday_list')


def save_holiday_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            holidays = Holiday.objects.all()
            data['html_holiday_list'] = render_to_string('holidays/includes/partial_holiday_list.html', {
                'holidays': holidays
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def holiday_view(request, holiday_pk):
    holiday = get_object_or_404(Holiday, pk=holiday_pk)
    if request.method == 'POST':
        form = HolidayForm(request.POST, instance=holiday)
    else:
        form = HolidayForm(instance=holiday)
    return save_vehicle_form(request, form, 'holidays/includes/partial_holiday_view.html')


def holiday_delete(request, holiday_pk):
    holiday = get_object_or_404(Holiday, pk=holiday_pk)
    data = dict()
    if request.method == 'POST':
        holiday.delete()
        data['form_is_valid'] = True
        holidays = Holiday.objects.all()
        data['html_holiday_list'] = render_to_string('holidays/includes/partial_holiday_list.html', {
            'holidays': holidays
        })
    else:
        context = {'holiday': holiday}
        data['html_form'] = render_to_string('holidays/includes/partial_holiday_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF HOLIDAY MODULE<===##################################################

# ###################################===>BEGINNING OF EVENT MODULE<===###############################################


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'


class EventCreateView(CreateView):
    model = Event
    template_name = 'events/event_create.html'
    fields = ('event_title', 'event_for', 'event_place', 'from_date', 'to_date', 'image', 'note',
              'Is_View_on_Web')

    def get_form(self):
        form = super().get_form()
        form.fields['from_date'].widget = DatePickerInput()
        form.fields['to_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        event = form.save(commit=False)
        event.save()
        return redirect('event_list')


class EventUpdateView(UpdateView):
    model = Event
    template_name = 'events/update_event.html'
    pk_url_kwarg = 'event_pk'
    fields = ('event_title', 'event_for', 'event_place', 'from_date', 'to_date', 'image', 'note',
              'Is_View_on_Web')

    def get_form(self):
        form = super().get_form()
        form.fields['from_date'].widget = DatePickerInput()
        form.fields['to_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        event = form.save(commit=False)
        event.save()
        return redirect('event_list')


def save_event_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            events = Event.objects.all()
            data['html_event_list'] = render_to_string('events/includes/partial_event_list.html', {
                'events': events
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def event_view(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
    else:
        form = EventForm(instance=event)
    return save_vehicle_form(request, form, 'events/includes/partial_event_view.html')


def event_delete(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    data = dict()
    if request.method == 'POST':
        event.delete()
        data['form_is_valid'] = True
        events = Event.objects.all()
        data['html_event_list'] = render_to_string('events/includes/partial_event_list.html', {
            'events': events
        })
    else:
        context = {'event': event}
        data['html_form'] = render_to_string('events/includes/partial_event_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF EVENT MODULE<===##################################################

# ###################################===>BEGINNING OF TYPE MODULE<===###############################################


class TypeListView(ListView):
    model = Type
    template_name = 'types/type_list.html'
    context_object_name = 'types'


class TypeCreateView(CreateView):
    model = Type
    template_name = 'types/type_create.html'
    fields = ['complain_type']

    def form_valid(self, form):
        type = form.save(commit=False)
        type.save()
        return redirect('type_list')


class TypeUpdateView(UpdateView):
    model = Type
    template_name = 'types/update_type.html'
    pk_url_kwarg = 'type_pk'
    fields = ('complain_type',)

    def form_valid(self, form):
        type = form.save(commit=False)
        type.save()
        return redirect('type_list')


def save_type_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            types = Type.objects.all()
            data['html_type_list'] = render_to_string('types/includes/partial_type_list.html', {
                'types': types
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def type_delete(request, type_pk):
    type = get_object_or_404(Type, pk=type_pk)
    data = dict()
    if request.method == 'POST':
        type.delete()
        data['form_is_valid'] = True
        types = Type.objects.all()
        data['html_type_list'] = render_to_string('types/includes/partial_type_list.html', {
            'types': types
        })
    else:
        context = {'type': type}
        data['html_form'] = render_to_string('types/includes/partial_type_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF TYPE MODULE<===##################################################

# ###################################===>BEGINNING OF COMPLAIN MODULE<===###############################################


class ComplainListView(ListView):
    model = Complain
    template_name = 'complains/complain_list.html'
    context_object_name = 'complains'


class ComplainCreateView(CreateView):
    model = Complain
    template_name = 'complains/complain_create.html'
    fields = ('complain_user_type', 'complain_user', 'complain_type', 'complain_date', 'complain',
              'action_date')

    def get_form(self):
        form = super().get_form()
        form.fields['complain_date'].widget = DatePickerInput()
        form.fields['action_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        complain = form.save(commit=False)
        complain.save()
        return redirect('complain_list')


class ComplainUpdateView(UpdateView):
    model = Complain
    template_name = 'complains/update_complain.html'
    pk_url_kwarg = 'complain_pk'
    fields = ('complain_user_type', 'complain_user', 'complain_type', 'complain_date', 'complain',
              'action_date')

    def get_form(self):
        form = super().get_form()
        form.fields['complain_date'].widget = DatePickerInput()
        form.fields['action_date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        complain = form.save(commit=False)
        complain.save()
        return redirect('complain_list')


def save_complain_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            complains = Complain.objects.all()
            data['html_complain_list'] = render_to_string('complains/includes/partial_complain_list.html', {
                'complains': complains
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def complain_view(request, complain_pk):
    complain = get_object_or_404(Complain, pk=complain_pk)
    if request.method == 'POST':
        form = ComplainForm(request.POST, instance=complain)
    else:
        form = ComplainForm(instance=complain)
    return save_vehicle_form(request, form, 'complains/includes/partial_complain_view.html')


def complain_delete(request, complain_pk):
    complain = get_object_or_404(Complain, pk=complain_pk)
    data = dict()
    if request.method == 'POST':
        complain.delete()
        data['form_is_valid'] = True
        complains = Complain.objects.all()
        data['html_complain_list'] = render_to_string('complains/includes/partial_complain_list.html', {
            'complains': complains
        })
    else:
        context = {'complain': complain}
        data['html_form'] = render_to_string('complains/includes/partial_complain_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF COMPLAIN MODULE<===################################################


# ###################################===>BEGINNING OF VISITOR MODULE<===###############################################


class VisitorListView(ListView):
    model = Visitor
    template_name = 'visitors/visitor_list.html'
    context_object_name = 'visitors'


class VisitorCreateView(CreateView):
    model = Visitor
    template_name = 'visitors/visitor_create.html'
    fields = ('name', 'phone', 'to_meet_user_type', 'to_meet_user', 'visitor_purpose', 'note')

    def form_valid(self, form):
        visitor = form.save(commit=False)
        visitor.save()
        return redirect('visitor_list')


class VisitorUpdateView(UpdateView):
    model = Visitor
    template_name = 'visitors/update_visitor.html'
    pk_url_kwarg = 'visitor_pk'
    fields = ('name', 'phone', 'to_meet_user_type', 'to_meet_user', 'visitor_purpose', 'note')

    def form_valid(self, form):
        visitor = form.save(commit=False)
        visitor.save()
        return redirect('visitor_list')


def check_out(request, visitor_pk):
    visitor = Visitor.objects.get(pk=visitor_pk)
    visitor.check_out = datetime.now()
    visitor.save()
    messages.success(request, "Visitor has been successfully checked out!")
    return redirect('visitor_list')


def save_visitor_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            visitors = Visitor.objects.all()
            data['html_visitor_list'] = render_to_string('visitors/includes/partial_visitor_list.html', {
                'visitors': visitors
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def visitor_view(request, visitor_pk):
    visitor = get_object_or_404(Visitor, pk=visitor_pk)
    if request.method == 'POST':
        form = VisitorForm(request.POST, instance=visitor)
    else:
        form = VisitorForm(instance=visitor)
    return save_visitor_form(request, form, 'visitors/includes/partial_visitor_view.html')


def visitor_delete(request, visitor_pk):
    visitor = get_object_or_404(Visitor, pk=visitor_pk)
    data = dict()
    if request.method == 'POST':
        visitor.delete()
        data['form_is_valid'] = True
        visitors = Visitor.objects.all()
        data['html_visitor_list'] = render_to_string('visitors/includes/partial_visitor_list.html', {
            'visitors': visitors
        })
    else:
        context = {'visitor': visitor}
        data['html_form'] = render_to_string('visitors/includes/partial_visitor_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF VISITOR MODULE<===###########################################

# #######################################===>BEGINNING OF SALARY GRADE<===########################################


class SalaryGradeListView(ListView):
    model = SalaryGrade
    template_name = 'salary_grades/salary_grade_list.html'
    context_object_name = 'salary_grades'


def salary_grade_create(request):
    if request.method == "POST":
        form = SalaryGradeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('salary_grade_list')
    else:
        form = SalaryGradeForm()
        context = {'form': form}
        return render(request, 'salary_grades/salary_grade_create.html', context)


class SalaryGradeUpdateView(UpdateView):
    model = SalaryGrade
    template_name = 'salary_grades/salary_grade_update.html'
    pk_url_kwarg = 'salary_pk'
    fields = ('grade_name', 'basic_salary', 'house_rent', 'transport_allowance', 'medical_allowance',
              'over_time_hourly_pay', 'provident_fund', 'hourly_rate', 'total_allowance',
              'total_deduction', 'gross_salary', 'net_salary', 'note')

    def form_valid(self, form):
        salary = form.save(commit=False)
        salary.save()
        return redirect('salary_grade_list')


def save_salary_grade_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            salary_grades = SalaryGrade.objects.all()
            data['html_salary_grade_list'] = render_to_string('salary_grades/includes/partial_salary_grade_list.html', {
                'salary_grades': salary_grades
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def salary_grade_view(request, salary_pk):
    salary_grade = get_object_or_404(SalaryGrade, pk=salary_pk)
    if request.method == 'POST':
        form = SalaryGradeForm(request.POST, instance=salary_grade)
    else:
        form = SalaryGradeForm(instance=salary_grade)
    return save_salary_grade_form(request, form, 'salary_grades/includes/partial_salary_grade_view.html')


def salary_grade_delete(request, salary_pk):
    salary_grade = get_object_or_404(SalaryGrade, pk=salary_pk)
    data = dict()
    if request.method == 'POST':
        salary_grade.delete()
        data['form_is_valid'] = True
        salary_grades = SalaryGrade.objects.all()
        data['html_salary_grade_list'] = render_to_string('salary_grades/includes/partial_salary_grade_list.html', {
            'salary_grades': salary_grades
        })
    else:
        context = {'salary_grade': salary_grade}
        data['html_form'] = render_to_string('salary_grades/includes/partial_salary_grade_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF SALARY GRADE<===#############################################

# #######################################===>BEGINNING OF DISCOUNT GRADE<===########################################


class DiscountListView(ListView):
    model = Discounting
    template_name = 'discounts/discount_list.html'
    context_object_name = 'discounts'


class DiscountCreateView(CreateView):
    model = Discounting
    template_name = 'discounts/discount_create.html'
    fields = ('title', 'amount', 'note')

    def form_valid(self, form):
        discount = form.save(commit=False)
        discount.save()
        return redirect('discount_list')


class DiscountUpdateView(UpdateView):
    model = Discounting
    template_name = 'discounts/update_discount.html'
    pk_url_kwarg = 'discount_pk'
    fields = ('title', 'amount', 'note')

    def form_valid(self, form):
        discount = form.save(commit=False)
        discount.save()
        return redirect('discount_list')


def save_discount_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            discounts = Discounting.objects.all()
            data['html_discount_list'] = render_to_string('discounts/includes/partial_discount_list.html', {
                'discounts': discounts
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def discount_delete(request, discount_pk):
    discount = get_object_or_404(Discounting, pk=discount_pk)
    data = dict()
    if request.method == 'POST':
        discount.delete()
        data['form_is_valid'] = True
        discounts = Discounting.objects.all()
        data['html_discount_list'] = render_to_string('discounts/includes/partial_discount_list.html', {
            'discounts': discounts
        })
    else:
        context = {'discount': discount}
        data['html_form'] = render_to_string('discounts/includes/partial_discount_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF DISCOUNT MODULE<===############################################

# #######################################===>BEGINNING OF FEE TYPE MODULE<===######################################


class FeeTypeListView(ListView):
    model = FeeType
    template_name = 'fee_types/fee_type_list.html'
    context_object_name = 'fee_types'


# def create_fees_type(request):
#     if request.method == "POST":
#         form = FeeTypeForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('fee_type_list')
#     else:
#         form = FeeTypeForm()
#         fees = FeeType.objects.all()
#         context = {'form': form, 'fees': fees}
#         return render(request, 'fee_types/create_fees_type.html', context)


class FeeTypeCreateView(CreateView):
    model = FeeType
    template_name = 'fee_types/fee_type_create.html'
    fields = ('fee_type', 'fee_title', 'note')

    def form_valid(self, form):
        fee_type = form.save(commit=False)
        fee_type.save()
        return redirect('fee_type_list')


class FeeTypeUpdateView(UpdateView):
    model = FeeType
    template_name = 'fee_types/update_fee_type.html'
    pk_url_kwarg = 'fee_type_pk'
    fields = ('fee_type', 'fee_title', 'note')

    def form_valid(self, form):
        fee_type = form.save(commit=False)
        fee_type.save()
        return redirect('fee_type_list')


def save_fee_type_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            fee_types = FeeType.objects.all()
            data['html_fee_type_list'] = render_to_string('fee_types/includes/partial_fee_type_list.html', {
                'fee_types': fee_types
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def fee_type_delete(request, fee_type_pk):
    fee_type = get_object_or_404(FeeType, pk=fee_type_pk)
    data = dict()
    if request.method == 'POST':
        fee_type.delete()
        data['form_is_valid'] = True
        fee_types = FeeType.objects.all()
        data['html_fee_type_list'] = render_to_string('fee_types/includes/partial_fee_type_list.html', {
            'fee_types': fee_types
        })
    else:
        context = {'fee_type': fee_type}
        data['html_form'] = render_to_string('fee_types/includes/partial_fee_type_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF FEE TYPE MODULE<===############################################

# #######################################===>BEGINNING OF INVOICE MODULE<===######################################


class InvoiceListView(ListView):
    model = Invoice
    template_name = 'invoices/invoice_list.html'
    context_object_name = 'invoices'


def invoice_create(request):
    form = InvoiceForm(request.POST or None, request.FILES or None)
    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = MonthPickerInput()

        return form
    if form.is_valid():
        invoice = form.save(commit=False)
        invoice.save()
        invoice.school = form.cleaned_data.get('school')
        invoice.classroom = form.cleaned_data.get('classroom')
        invoice.student = form.cleaned_data.get('student')
        invoice.fee_type = form.cleaned_data.get('fee_type')
        invoice.fee_amount = form.cleaned_data.get('fee_amount')
        invoice.discount = form.cleaned_data.get('discount')
        invoice.month = form.cleaned_data.get('month')
        invoice.paid_status = form.cleaned_data.get('paid_status')
        invoice.invoice_number = form.cleaned_data.get('invoice_number')
        invoice.note = form.cleaned_data.get('note')
        invoice.net_amount = form.cleaned_data.get('net_amount')
        invoice.save()
        invoice_url = reverse('invoice_list')
        return redirect(invoice_url)
    context = {'form': form}
    return render(request, 'invoices/create_invoice.html', context)


class InvoiceUpdateView(UpdateView):
    model = Invoice
    template_name = 'invoices/update_invoice.html'
    pk_url_kwarg = 'invoice_pk'
    fields = ('classroom', 'student', 'fee_type', 'fee_amount', 'discount', 'note')

    def form_valid(self, form):
        invoice = form.save(commit=False)
        invoice.save()
        return redirect('invoice_list')


def save_invoice_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            invoices = Invoice.objects.all()
            data['html_invoice_list'] = render_to_string('invoices/includes/partial_invoice_list.html', {
                'invoices': invoices
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def invoice_view(request, invoice_pk):
    invoice = get_object_or_404(Invoice, pk=invoice_pk)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
    else:
        form = InvoiceForm(instance=invoice)
    context = {'form': form}
    return render(request, 'invoices/invoice_view.html', context)


def invoice_delete(request, invoice_pk):
    invoice = get_object_or_404(Invoice, pk=invoice_pk)
    data = dict()
    if request.method == 'POST':
        invoice.delete()
        data['form_is_valid'] = True
        invoices = Invoice.objects.all()
        data['html_invoice_list'] = render_to_string('invoices/includes/partial_invoice_list.html', {
            'invoices': invoices
        })
    else:
        context = {'invoice': invoice}
        data['html_form'] = render_to_string('invoices/includes/partial_invoice_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


def paying_fees(request, pk):
    items = get_object_or_404(Invoice, student_id=pk)
    # add a second condition to fetch only school fees exclude other dues
    if request.method == "POST":
        form = UpdateInvoiceForm(request.POST, request.FILES, instance=items)
        if form.is_valid():
            form.save()
            return redirect('invoice_list')
    else:
        form = InvoiceForm(instance=items)
        students = Student.objects.filter(id__in=pk)
        context = {'form': form, 'students': students}
        return render(request, 'invoices/paying_fees_update.html', context)


# #######################################===>END OF INVOICE MODULE<===############################################

# #######################################===>BEGINNING OF BULK INVOICE MODULE<===######################################


def bulk_invoice_list(request):
    bulk_invoices = BulkInvoice.objects.all()
    return render(request, 'bulk_invoices/bulk_invoice_list.html', {'bulk_invoices': bulk_invoices})


def save_bulk_invoice_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            bulk_invoices = BulkInvoice.objects.all()
            data['html_bulk_invoice_list'] = render_to_string('bulk_invoices/includes/partial_bulk_invoice_list.html', {
                'bulk_invoices': bulk_invoices
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def bulk_invoice_create(request):
    if request.method == 'POST':
        form = BulkInvoiceForm(request.POST)
    else:
        form = BulkInvoiceForm()
    return save_bulk_invoice_form(request, form, 'bulk_invoices/includes/partial_bulk_invoice_create.html')


def bulk_invoice_update(request, pk):
    bulk_invoice = get_object_or_404(BulkInvoice, pk=pk)
    if request.method == 'POST':
        form = BulkInvoiceForm(request.POST, instance=bulk_invoice)
    else:
        form = BulkInvoiceForm(instance=bulk_invoice)
    return save_bulk_invoice_form(request, form, 'bulk_invoices/includes/partial_bulk_invoice_update.html')


def bulk_invoice_delete(request, pk):
    bulk_invoice = get_object_or_404(BulkInvoice, pk=pk)
    data = dict()
    if request.method == 'POST':
        bulk_invoice.delete()
        data['form_is_valid'] = True
        bulk_invoices = BulkInvoice.objects.all()
        data['html_bulk_invoice_list'] = render_to_string('bulk_invoices/includes/partial_bulk_invoice_list.html', {
            'bulk_invoices': bulk_invoices
        })
    else:
        context = {'bulk_invoice': bulk_invoice}
        data['html_form'] = render_to_string('bulk_invoices/includes/partial_bulk_invoice_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF BULK INVOICE MODULE<===#############################################

# #######################################===>BEGINNING OF DUE FEE MODULE<===######################################


def student_dues_paid(request):
    if request.method == "POST":
        form = PaidDuesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dues_paid_list')
        else:
            form = PaidDuesForm()
            return render(request, 'invoices/paying_fees_update.html', {'form': form})


def dues_paid_list(request):
    context = {}
    invoices = Invoice.objects.all()
    lists = PaidDues.objects.all().order_by('student_id')
    context['lists'] = lists
    return render(request, 'invoices/paid_dues_list.html', context)


# #######################################===>END OF DUE FEE MODULE<===################################################

# ###################################===>BEGINNING OF DUE FEE EMAIL MODULE<===#########################################


def due_fee_list(request):
    invoices = Invoice.objects.filter(Q(paid_status='UNPAID') | Q(paid_status='PARTIAL'))
    context = {'invoices': invoices}
    return render(request, 'invoices/due_list.html', context)


class DueEmailListView(ListView):
    model = DueFeeEmail
    template_name = 'due_fee_emails/due_fee_email_list.html'
    context_object_name = 'due_fee_emails'


class DueEmailCreateView(CreateView):
    model = DueFeeEmail
    template_name = 'due_fee_emails/due_fee_email_create.html'
    fields = ('receiver_role', 'classroom', 'due_fee_student', 'template', 'subject', 'email_body',
              'attachment')

    def form_valid(self, form):
        due_fee_emails = form.save(commit=False)
        due_fee_emails.save()
        return redirect('due_fee_email_list')


def save_due_fee_email_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            due_fee_emails = DueFeeEmail.objects.all()
            data['html_due_fee_email_list'] = render_to_string(
                'due_fee_emails/includes/partial_due_fee_email_list.html', {
                    'due_fee_emails': due_fee_emails
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def due_fee_email_view(request, due_fee_email_pk):
    due_fee_email = get_object_or_404(DueFeeEmail, pk=due_fee_email_pk)
    if request.method == 'POST':
        form = DueFeeEmailForm(request.POST, instance=due_fee_email)
    else:
        form = DueFeeEmailForm(instance=due_fee_email)
    return save_due_fee_email_form(request, form, 'due_fee_emails/includes/partial_due_fee_email_view.html')


def due_fee_email_delete(request, due_fee_email_pk):
    due_fee_email = get_object_or_404(DueFeeEmail, pk=due_fee_email_pk)
    data = dict()
    if request.method == 'POST':
        due_fee_email.delete()
        data['form_is_valid'] = True
        due_fee_emails = DueFeeEmail.objects.all()
        data['html_due_fee_email_list'] = render_to_string('due_fee_emails/includes/partial_due_fee_email_list.html', {
            'due_fee_emails': due_fee_emails
        })
    else:
        context = {'due_fee_email': due_fee_email}
        data['html_form'] = render_to_string('due_fee_emails/includes/partial_due_fee_email_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF DUE FEE EMAIL MODULE<===###########################################

# ###################################===>BEGINNING OF DUE FEE SMS MODULE<===###########################################


class DueSmsListView(ListView):
    model = DueFeeSMS
    template_name = 'due_fee_smss/due_fee_sms_list.html'
    context_object_name = 'due_fee_smss'


class DueSmsCreateView(CreateView):
    model = DueFeeSMS
    template_name = 'due_fee_smss/due_fee_sms_create.html'
    fields = ('receiver_type', 'classroom', 'due_fee_student', 'template', 'SMS', 'gateway')

    def form_valid(self, form):
        due_fee_smss = form.save(commit=False)
        due_fee_smss.save()
        return redirect('due_fee_sms_list')


def save_due_fee_sms_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            due_fee_smss = DueFeeSMS.objects.all()
            data['html_due_fee_sms_list'] = render_to_string('due_fee_smss/includes/partial_due_fee_sms_list.html', {
                'due_fee_smss': due_fee_smss
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def due_fee_sms_view(request, due_fee_sms_pk):
    due_fee_sms = get_object_or_404(DueFeeSMS, pk=due_fee_sms_pk)
    if request.method == 'POST':
        form = DueFeeSMSForm(request.POST, instance=due_fee_sms)
    else:
        form = DueFeeSMSForm(instance=due_fee_sms)
    return save_due_fee_sms_form(request, form, 'due_fee_smss/includes/partial_due_fee_sms_view.html')


def due_fee_sms_delete(request, due_fee_sms_pk):
    due_fee_sms = get_object_or_404(DueFeeSMS, pk=due_fee_sms_pk)
    data = dict()
    if request.method == 'POST':
        due_fee_sms.delete()
        data['form_is_valid'] = True
        due_fee_smss = DueFeeSMS.objects.all()
        data['html_due_fee_sms_list'] = render_to_string('due_fee_smss/includes/partial_due_fee_sms_list.html', {
            'due_fee_smss': due_fee_smss
        })
    else:
        context = {'due_fee_sms': due_fee_sms}
        data['html_form'] = render_to_string('due_fee_smss/includes/partial_due_fee_sms_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF DUE FEE SMS MODULE<===#############################################

# ###################################===>BEGINNING OF INCOME HEAD MODULE<===###########################################


class IncomeHeadListView(ListView):
    model = IncomeHead
    template_name = 'income_heads/income_head_list.html'
    context_object_name = 'income_heads'


class IncomeHeadCreateView(CreateView):
    model = IncomeHead
    template_name = 'income_heads/income_head_create.html'
    fields = ('income_head', 'note')

    def form_valid(self, form):
        income_head = form.save(commit=False)
        income_head.save()
        return redirect('income_head_list')


class IncomeHeadUpdateView(UpdateView):
    model = IncomeHead
    template_name = 'income_heads/update_income_head.html'
    pk_url_kwarg = 'income_head_pk'
    fields = ('income_head', 'note')

    def form_valid(self, form):
        income_head = form.save(commit=False)
        income_head.save()
        return redirect('income_head_list')


def save_income_head_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            income_heads = IncomeHead.objects.all()
            data['html_income_head_list'] = render_to_string('income_heads/includes/partial_income_head_list.html', {
                'income_heads': income_heads
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def income_head_delete(request, income_head_pk):
    income_head = get_object_or_404(IncomeHead, pk=income_head_pk)
    data = dict()
    if request.method == 'POST':
        income_head.delete()
        data['form_is_valid'] = True
        income_heads = IncomeHead.objects.all()
        data['html_income_head_list'] = render_to_string('income_heads/includes/partial_income_head_list.html', {
            'income_heads': income_heads
        })
    else:
        context = {'income_head': income_head}
        data['html_form'] = render_to_string('income_heads/includes/partial_income_head_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF INCOME HEAD MODULE<===#############################################

# ###################################===>BEGINNING OF INCOME MODULE<===###############################################


class IncomeListView(ListView):
    model = Income
    template_name = 'incomes/income_list.html'
    context_object_name = 'incomes'


class IncomeCreateView(CreateView):
    model = Income
    template_name = 'incomes/income_create.html'
    fields = ('income_head', 'payment_method', 'amount', 'date', 'note')

    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        income = form.save(commit=False)
        income.save()
        return redirect('income_list')


class IncomeUpdateView(UpdateView):
    model = Income
    template_name = 'incomes/update_income.html'
    pk_url_kwarg = 'income_pk'
    fields = ('income_head', 'payment_method', 'amount', 'date', 'note')

    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        income = form.save(commit=False)
        income.save()
        return redirect('income_list')


def save_income_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            incomes = Income.objects.all()
            data['html_income_list'] = render_to_string('incomes/includes/partial_income_list.html', {
                'incomes': incomes
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def income_view(request, income_pk):
    income = get_object_or_404(Income, pk=income_pk)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
    else:
        form = IncomeForm(instance=income)
    return save_income_form(request, form, 'incomes/includes/partial_income_view.html')


def income_delete(request, income_pk):
    income = get_object_or_404(Income, pk=income_pk)
    data = dict()
    if request.method == 'POST':
        income.delete()
        data['form_is_valid'] = True
        incomes = Income.objects.all()
        data['html_income_list'] = render_to_string('incomes/includes/partial_income_list.html', {
            'incomes': incomes
        })
    else:
        context = {'income': income}
        data['html_form'] = render_to_string('incomes/includes/partial_income_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF INCOME MODULE<===#############################################

# ###################################===>BEGINNING OF EXPENDITURE HEAD MODULE<===#####################################


class ExpenditureHeadListView(ListView):
    model = ExpenditureHead
    template_name = 'expenditure_heads/expenditure_head_list.html'
    context_object_name = 'expenditure_heads'


class ExpenditureHeadCreateView(CreateView):
    model = ExpenditureHead
    template_name = 'expenditure_heads/expenditure_head_create.html'
    fields = ('expenditure_head', 'note')

    def form_valid(self, form):
        expenditure_head = form.save(commit=False)
        expenditure_head.save()
        return redirect('expenditure_head_list')


class ExpenditureHeadUpdateView(UpdateView):
    model = ExpenditureHead
    template_name = 'expenditure_heads/update_expenditure_head.html'
    pk_url_kwarg = 'expenditure_head_pk'
    fields = ('expenditure_head', 'note')

    def form_valid(self, form):
        expenditure_head = form.save(commit=False)
        expenditure_head.save()
        return redirect('expenditure_head_list')


def save_expenditure_head_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            expenditure_heads = ExpenditureHead.objects.all()
            data['html_expenditure_head_list'] = render_to_string(
                'expenditure_heads/includes/partial_expenditure_head_list.html', {
                    'expenditure_heads': expenditure_heads
                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def expenditure_head_delete(request, expenditure_head_pk):
    expenditure_head = get_object_or_404(ExpenditureHead, pk=expenditure_head_pk)
    data = dict()
    if request.method == 'POST':
        expenditure_head.delete()
        data['form_is_valid'] = True
        expenditure_heads = ExpenditureHead.objects.all()
        data['html_expenditure_head_list'] = render_to_string(
            'expenditure_heads/includes/partial_expenditure_head_list.html', {
                'expenditure_heads': expenditure_heads
            })
    else:
        context = {'expenditure_head': expenditure_head}
        data['html_form'] = render_to_string('expenditure_heads/includes/partial_expenditure_head_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF EXPENDITURE HEAD MODULE<===########################################

# ###################################===>BEGINNING OF EXPENDITURE MODULE<===###########################################


class ExpenditureListView(ListView):
    model = Expenditure
    template_name = 'expenditures/expenditure_list.html'
    context_object_name = 'expenditures'


class ExpenditureCreateView(CreateView):
    model = Expenditure
    template_name = 'expenditures/expenditure_create.html'
    fields = ('expenditure_head', 'expenditure_method', 'amount', 'date', 'note')

    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        expenditure = form.save(commit=False)
        expenditure.save()
        return redirect('expenditure_list')


class ExpenditureUpdateView(UpdateView):
    model = Expenditure
    template_name = 'expenditures/update_expenditure.html'
    pk_url_kwarg = 'expenditure_pk'
    fields = ('expenditure_head', 'expenditure_method', 'amount', 'date', 'note')

    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        expenditure = form.save(commit=False)
        expenditure.save()
        return redirect('expenditure_list')


def save_expenditure_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            expenditures = Expenditure.objects.all()
            data['html_expenditure_list'] = render_to_string('expenditures/includes/partial_expenditure_list.html', {
                'expenditures': expenditures
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def expenditure_view(request, expenditure_pk):
    expenditure = get_object_or_404(Expenditure, pk=expenditure_pk)
    if request.method == 'POST':
        form = ExpenditureForm(request.POST, instance=expenditure)
    else:
        form = ExpenditureForm(instance=expenditure)
    return save_expenditure_form(request, form, 'expenditures/includes/partial_expenditure_view.html')


def expenditure_delete(request, expenditure_pk):
    expenditure = get_object_or_404(Expenditure, pk=expenditure_pk)
    data = dict()
    if request.method == 'POST':
        expenditure.delete()
        data['form_is_valid'] = True
        expenditures = Expenditure.objects.all()
        data['html_expenditure_list'] = render_to_string('expenditures/includes/partial_expenditure_list.html', {
            'expenditures': expenditures
        })
    else:
        context = {'expenditure': expenditure}
        data['html_form'] = render_to_string('expenditures/includes/partial_expenditure_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF EXPENDITURE MODULE<===#############################################

# ###################################===>BEGINNING OF GALLERY MODULE<===###############################################


class GalleryListView(ListView):
    model = Gallery
    template_name = 'galleries/gallery_list.html'
    context_object_name = 'galleries'


class GalleryCreateView(CreateView):
    model = Gallery
    template_name = 'galleries/gallery_create.html'
    fields = ('gallery_title', 'note', 'Is_View_on_Web')

    def form_valid(self, form):
        gallery = form.save(commit=False)
        gallery.save()
        return redirect('gallery_list')


class GalleryUpdateView(UpdateView):
    model = Gallery
    template_name = 'galleries/update_gallery.html'
    pk_url_kwarg = 'gallery_pk'
    fields = ('gallery_title', 'note', 'Is_View_on_Web')

    def form_valid(self, form):
        gallery = form.save(commit=False)
        gallery.save()
        return redirect('gallery_list')


def save_gallery_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            gallerys = Gallery.objects.all()
            data['html_gallery_list'] = render_to_string('galleries/includes/partial_gallery_list.html', {
                'galleries': gallerys
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def gallery_delete(request, gallery_pk):
    gallery = get_object_or_404(Gallery, pk=gallery_pk)
    data = dict()
    if request.method == 'POST':
        gallery.delete()
        data['form_is_valid'] = True
        gallerys = Gallery.objects.all()
        data['html_gallery_list'] = render_to_string('galleries/includes/partial_gallery_list.html', {
            'galleries': gallerys
        })
    else:
        context = {'gallery': gallery}
        data['html_form'] = render_to_string('galleries/includes/partial_gallery_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF GALLERY MODULE<===##################################################

# ###################################===>BEGINNING OF IMAGE MODULE<===###############################################


class ImageListView(ListView):
    model = Image
    template_name = 'images/image_list.html'
    context_object_name = 'images'


class ImageCreateView(CreateView):
    model = Image
    template_name = 'images/image_create.html'
    fields = ('gallery_title', 'gallery_image', 'image_caption')

    def form_valid(self, form):
        image = form.save(commit=False)
        image.save()
        return redirect('image_list')


class ImageUpdateView(UpdateView):
    model = Image
    template_name = 'images/update_image.html'
    pk_url_kwarg = 'image_pk'
    fields = ('gallery_title', 'gallery_image', 'image_caption')

    def form_valid(self, form):
        image = form.save(commit=False)
        image.save()
        return redirect('image_list')


def save_image_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            images = Image.objects.all()
            data['html_image_list'] = render_to_string('images/includes/partial_image_list.html', {
                'images': images
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def image_view(request, image_pk):
    image = get_object_or_404(Image, pk=image_pk)
    if request.method == 'POST':
        form = ImageForm(request.POST, instance=image)
    else:
        form = ImageForm(instance=image)
    return save_image_form(request, form, 'images/includes/partial_image_view.html')


def image_delete(request, image_pk):
    image = get_object_or_404(Image, pk=image_pk)
    data = dict()
    if request.method == 'POST':
        image.delete()
        data['form_is_valid'] = True
        images = Image.objects.all()
        data['html_image_list'] = render_to_string('images/includes/partial_image_list.html', {
            'images': images
        })
    else:
        context = {'image': image}
        data['html_form'] = render_to_string('images/includes/partial_image_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF IMAGE MODULE<===##################################################

# ###################################===>BEGINNING OF PAGE MODULE<===###############################################


class PageListView(ListView):
    model = Page
    template_name = 'pages/page_list.html'
    context_object_name = 'pages'


class PageCreateView(CreateView):
    model = Page
    template_name = 'pages/page_create.html'
    fields = ('page_location', 'page_title', 'page_description', 'page_image')

    def form_valid(self, form):
        page = form.save(commit=False)
        page.save()
        return redirect('page_list')


class PageUpdateView(UpdateView):
    model = Page
    template_name = 'pages/update_page.html'
    pk_url_kwarg = 'page_pk'
    fields = ('page_location', 'page_title', 'page_description', 'page_image')

    def form_valid(self, form):
        page = form.save(commit=False)
        page.save()
        return redirect('page_list')


def save_page_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            pages = Page.objects.all()
            data['html_page_list'] = render_to_string('pages/includes/partial_page_list.html', {
                'pages': pages
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def page_view(request, page_pk):
    page = get_object_or_404(Page, pk=page_pk)
    if request.method == 'POST':
        form = PageForm(request.POST, instance=page)
    else:
        form = PageForm(instance=page)
    return save_page_form(request, form, 'pages/includes/partial_page_view.html')


def page_delete(request, page_pk):
    page = get_object_or_404(Page, pk=page_pk)
    data = dict()
    if request.method == 'POST':
        page.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        pages = Page.objects.all()
        data['html_page_list'] = render_to_string('pages/includes/partial_page_list.html', {
            'pages': pages
        })
    else:
        context = {'page': page}
        data['html_form'] = render_to_string('pages/includes/partial_page_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF PAGE MODULE<===##################################################

# ###################################===>BEGINNING OF SLIDER MODULE<===###############################################


class SliderListView(ListView):
    model = Slider
    template_name = 'sliders/slider_list.html'
    context_object_name = 'sliders'


class SliderCreateView(CreateView):
    model = Slider
    template_name = 'sliders/slider_create.html'
    fields = ('slider_image', 'image_title')

    def form_valid(self, form):
        slider = form.save(commit=False)
        slider.save()
        return redirect('slider_list')


class SliderUpdateView(UpdateView):
    model = Slider
    template_name = 'sliders/update_slider.html'
    pk_url_kwarg = 'slider_pk'
    fields = ('slider_image', 'image_title')

    def form_valid(self, form):
        slider = form.save(commit=False)
        slider.save()
        return redirect('slider_list')


def save_slider_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            sliders = Slider.objects.all()
            data['html_slider_list'] = render_to_string('sliders/includes/partial_slider_list.html', {
                'sliders': sliders
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def slider_view(request, slider_pk):
    slider = get_object_or_404(Slider, pk=slider_pk)
    if request.method == 'POST':
        form = SliderForm(request.POST, instance=slider)
    else:
        form = SliderForm(instance=slider)
    return save_slider_form(request, form, 'sliders/includes/partial_slider_view.html')


def slider_delete(request, slider_pk):
    slider = get_object_or_404(Slider, pk=slider_pk)
    data = dict()
    if request.method == 'POST':
        slider.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        sliders = Slider.objects.all()
        data['html_slider_list'] = render_to_string('sliders/includes/partial_slider_list.html', {
            'sliders': sliders
        })
    else:
        context = {'slider': slider}
        data['html_form'] = render_to_string('sliders/includes/partial_slider_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF SLIDER MODULE<===##################################################

# ###################################===>BEGINNING OF ABOUT MODULE<===###############################################


class AboutListView(ListView):
    model = About
    template_name = 'abouts/about_list.html'
    context_object_name = 'abouts'


class AboutCreateView(CreateView):
    model = About
    template_name = 'abouts/about_create.html'
    fields = ('about', 'about_image')

    def form_valid(self, form):
        about = form.save(commit=False)
        about.save()
        return redirect('about_list')


class AboutUpdateView(UpdateView):
    model = About
    template_name = 'abouts/update_about.html'
    pk_url_kwarg = 'about_pk'
    fields = ('about', 'about_image')

    def form_valid(self, form):
        about = form.save(commit=False)
        about.save()
        return redirect('about_list')


def save_about_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            abouts = About.objects.all()
            data['html_about_list'] = render_to_string('abouts/includes/partial_about_list.html', {
                'abouts': abouts
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def about_view(request, about_pk):
    about = get_object_or_404(About, pk=about_pk)
    if request.method == 'POST':
        form = AboutForm(request.POST, instance=about)
    else:
        form = AboutForm(instance=about)
    return save_about_form(request, form, 'abouts/includes/partial_about_view.html')


def about_delete(request, about_pk):
    about = get_object_or_404(About, pk=about_pk)
    data = dict()
    if request.method == 'POST':
        about.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        abouts = About.objects.all()
        data['html_about_list'] = render_to_string('abouts/includes/partial_about_list.html', {
            'abouts': abouts
        })
    else:
        context = {'about': about}
        data['html_form'] = render_to_string('abouts/includes/partial_about_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>END OF ABOUT MODULE<===##################################################


# ###################################===>BEGINNING OF PAYMENT MODULE<===###############################################


class PaymentSettingListView(ListView):
    model = Pesa
    template_name = 'payments/payment_setting_list.html'
    context_object_name = 'payments'


class PaypalCreateView(CreateView):
    model = Paypal
    template_name = 'payments/paypal_create.html'
    fields = ('paypal_email', 'is_demo', 'paypal_extra_charge', 'is_active', 'photo')

    def form_valid(self, form):
        payment = form.save(commit=False)
        payment.save()
        return redirect('payment_setting_list')


class PesaCreateView(CreateView):
    model = Pesa
    template_name = 'payments/pesa_create.html'
    fields = ('tel_no', 'is_active', 'photo')

    def form_valid(self, form):
        payment = form.save(commit=False)
        payment.save()
        return redirect('payment_setting_list')


class PaymentUpdateView(UpdateView):
    model = Payment
    template_name = 'payments/update_paypal.html'
    pk_url_kwarg = 'payment_pk'
    fields = ('paypal_email', 'is_demo', 'paypal_extra_charge', 'is_active', 'photo')

    def form_valid(self, form):
        payment = form.save(commit=False)
        payment.save()
        return redirect('payment_setting_list')


def save_payment_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            payments = Payment.objects.all()
            data['html_payment_list'] = render_to_string('payments/includes/partial_payment_list.html', {
                'payments': payments
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def payment_view(request, payment_pk):
    payment = get_object_or_404(Payment, pk=payment_pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
    else:
        form = PaymentForm(instance=payment)
    return save_payment_form(request, form, 'payments/includes/partial_payment_view.html')


def payment_delete(request, payment_pk):
    payment = get_object_or_404(Payment, pk=payment_pk)
    data = dict()
    if request.method == 'POST':
        payment.delete()
        data['form_is_valid'] = True
        payments = Payment.objects.all()
        data['html_payment_list'] = render_to_string('payments/includes/partial_payment_list.html', {
            'payments': payments
        })
    else:
        context = {'payment': payment}
        data['html_form'] = render_to_string('payments/includes/partial_payment_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


# #######################################===>BEGINNING OF SALARY PAYMENT MODULE<===####################################


def salary_payment(request):
    context = {}
    role = request.GET.get('role_type')
    context['form'] = SalaryPaymentForm(role)
    # Filter
    q = request.POST.get('payment_to')
    if q:
        q = q.replace('.', '')
        payee = User.objects.filter(id=str(q))
        context['payee'] = payee
    return render(request, 'payroll/salary_payment.html', context)


# retrieve employee instances from salary grade, add some other information and then save
def pay_employee(request, pk):
    gradeName = Employee.objects.get(id=pk)
    x = gradeName.salary_grade
    item = SalaryGrade.objects.filter(grade_name=x).first()
    # getting instance of the salary grade instance from the get method
    if request.method == "POST":
        form = SalaryGradeForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('salary_payment')
    else:
        form = SalaryGradeForm(instance=item)
        payee = Employee.objects.filter(id__in=pk)
        context = {'form': form, 'payee': payee}
        return render(request, 'payroll/pay_employees.html', context)


# retrieve employee instances from salary grade, add some other information and then save
def new_payment(request, pk):
    gradeName = Employee.objects.get(id=pk)
    x = gradeName.salary_grade
    item = SalaryGrade.objects.filter(
        grade_name=x).first()  # geting instance of the salary grade instance from the get method
    if request.method == "POST":
        form = SalaryGradeForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('SalaryPayment')
    else:
        form = SalaryGradeForm(instance=item)
        payee = Employee.objects.filter(id__in=pk)
        context = {'form': form, 'payee': payee}
        return render(request, 'payroll/pay_employees.html', context)


def Payment_List(request):
    list = SalaryGrade.objects.all()
    return render(request, 'payroll/Payment_List.html', {'list': list})


def EmployeeSalaryPaid(request):
    if request.method == "POST":
        form = MonthlySalaryPaidForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('SalaryReport')
        else:
            form = MonthlySalaryPaidForm()
            return render(request, 'payroll/pay_employees.html', {'form': form})


# retrieve employee instances from salary grade, add some other information and then save
def Pay_Employee(request, pk):
    gradeName = Employee.objects.get(id=pk)
    x = gradeName.salary_grade
    item = SalaryGrade.objects.filter(
        grade_name=x).first()  # geting instance of the salary grade instance from the get method
    if request.method == "POST":
        form = SalaryGradeForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('SalaryPayment')
    else:
        form = SalaryGradeForm(instance=item)
        payee = Employee.objects.filter(id__in=pk)
        context = {'form': form, 'payee': payee}
        return render(request, 'payroll/pay_employees.html', context)


def PaymentHistory(request):
    context = {}
    role = request.GET.get('role')
    form = SalaryPaymentForm(role)
    context = {'form': form}
    # Filter
    q = request.GET.get('employee')
    if q:
        history = MonthlySalaryPaid.objects.filter(employees_id=q).order_by('employee')

        context = {'history': history, 'q': q}
        return render(request, 'payroll/salary_payment_history.html', context)
    return render(request, 'payroll/salary_payment_index.html', context)


# #######################################===>END OF SALARY PAYMENT MODULE<===#########################################

# #######################################===>BEGINNING OF SETTINGS MODULE<===########################################


class SettingsCreateView(CreateView):
    model = Settings
    template_name = 'settings/create_settings.html'
    fields = ('brand_name', 'brand_title', 'language', 'enable_RTL', 'enable_Frontend', 'general_Theme',
              'default_time_zone', 'date_format', 'brand_logo', 'favicon_icon', 'brand_footer',
              'google_Analytics')

    def get_form(self):
        form = super().get_form()
        form.fields['date_format'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        settings = form.save(commit=False)
        settings.save()
        return redirect('settings_list')


class SettingsUpdateView(UpdateView):
    model = Settings
    template_name = 'settings/update_settings.html'
    pk_url_kwarg = 'settings_pk'
    fields = ('brand_name', 'brand_title', 'language', 'enable_RTL', 'enable_Frontend', 'general_Theme',
              'default_time_zone', 'date_format', 'brand_logo', 'favicon_icon', 'brand_footer',
              'google_Analytics')

    def get_form(self):
        form = super().get_form()
        form.fields['date_format'].widget = DatePickerInput()
        return form

    def form_valid(self, form):
        settings = form.save(commit=False)
        settings.save()
        return redirect('settings_list')


class SettingsListView(ListView):
    model = Settings
    template_name = 'settings/settings_list.html'
    context_object_name = 'settings'


def save_settings_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            settings = Settings.objects.all()
            data['html_settings_list'] = render_to_string('settings/includes/partial_settings_list.html', {
                'settings': settings
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


# ############################################===>END OF SETTINGS MODULE<===########################################

# ############################################===>BEGINNING OF REPORTS MODULE<===####################################

def EmployeeMonthlySalaryReport(request):
    reports = MonthlySalaryPaid.objects.all()
    return render(request, 'payroll/Payment_Report.html', {'reports': reports})


# IncomeReport
def income_report(request):
    context = {}
    form = IncomeForm()
    context = {'form': form}
    results = request.GET.get('payment_method')
    if results:
        ally = Income.objects.filter(payment_method=results)
        # testing = Income.objects.filter(payment_method=results).values('income_head')
        # .annotate(total_amount=Sum('amount')).order_by('income_head')
        x = Income.objects.filter(payment_method=results).aggregate(totals=models.Sum("amount"))
        (x['totals'])
        Amount = x["totals"]
        context = {'ally': ally, 'Amount': Amount}
        return render(request, 'reports/incomes_report_details.html', context)
    return render(request, 'reports/incomes_report.html', context)


# Expenditure Report
def expenditure_report(request):
    context = {}
    form = ExpenditureForm()
    context = {'form': form}
    results = request.GET.get('expenditure_method')
    if results:
        ally = Expenditure.objects.filter(expenditure_method=results)
        # testing = Income.objects.filter(payment_method=results).values('income_head')
        # .annotate(total_amount=Sum('amount')).order_by('income_head')
        x = Expenditure.objects.filter(expenditure_method=results).aggregate(totals=models.Sum("amount"))
        (x['totals'])
        Amount = x["totals"]
        context = {'ally': ally, 'Amount': Amount}
        return render(request, 'reports/expenditure_report_details.html', context)
    return render(request, 'reports/expenditure_report.html', context)


# Invoice Report
def invoices_report(request):
    context = {}
    form = InvoiceForm()
    context = {'form': form}
    feetypes = request.GET.get('fee_type')
    if feetypes:
        ally = Invoice.objects.filter(fee_type=feetypes)
        # testing = Income.objects.filter(payment_method=results).values('income_head')
        # .annotate(total_amount=Sum('amount')).order_by('income_head')
        x = Invoice.objects.filter(fee_type=feetypes).aggregate(totals=models.Sum("fee_amount"))
        (x['totals'])
        Amount = x["totals"]
        context = {'ally': ally, 'Amount': Amount}
        return render(request, 'Reports/feetype_invoice_report.html', context)
    return render(request, 'Reports/invoice_report_index.html', context)


# ############################################===>END OF REPORTS MODULE<===########################################

def theme(request):
    return render(request, 'home/theme.html')


def language(request):
    return render(request, 'home/language.html')


def classrooms_ajax(request):
    school = request.GET.get('school')
    classrooms = Classroom.objects.filter(school=school)
    context = {'classrooms': classrooms}
    return render(request, 'attendance/includes/_classrooms.html', context)


def classrooms_choices_ajax(request):
    school = request.GET.get('school')
    classrooms = Classroom.objects.filter(school=school)
    context = {'classrooms': classrooms}
    return render(request, 'attendance/includes/_classrooms_choices.html', context)


def sections_ajax(request):
    classroom = request.GET.get('classroom')
    sections = Section.objects.filter(classroom=classroom)
    context = {'sections': sections}
    return render(request, 'attendance/includes/_sections.html', context)


def sections_choices_ajax(request):
    classroom = request.GET.get('classroom')
    sections = Section.objects.filter(classroom=classroom)
    context = {'sections': sections}
    return render(request, 'attendance/includes/_sections_choices.html', context)


def load_classrooms(request):
    school_id = request.GET.get('school')
    classrooms = Classroom.objects.filter(school_id=school_id).order_by('classroom')
    return render(request, 'filter/classroom_dropdown_list_options.html', {'classrooms': classrooms})


def load_teachers(request):
    school_id = request.GET.get('school')
    teachers = Teacher.objects.filter(school_id=school_id).order_by('user')
    return render(request, 'filter/teacher_dropdown_list_options.html', {'teachers': teachers})


def load_employees(request):
    school_id = request.GET.get('school')
    employees = Employee.objects.filter(school_id=school_id).order_by('user')
    return render(request, 'filter/employee_dropdown_list_options.html', {'employees': employees})


def load_exams(request):
    school_id = request.GET.get('school')
    exams = Exam.objects.filter(school_id=school_id).order_by('exam_title')
    return render(request, 'filter/exam_dropdown_list_options.html', {'exams': exams})


# load fee type depending on a particular school selected.
def load_fee_types(request):
    class_id = request.GET.get('classroom')
    fee_types = FeeType.objects.filter(Class_id=class_id).order_by('Class')
    return render(request, 'filter/fee_dropdown_list_options.html', {'fee_types': fee_types})

    # load fee amount depending on the selection in fee types field


def load_fee_amount(request):
    feetype_id = request.GET.get('fee_type')
    fee_amounts = FeeType.objects.filter(id=feetype_id).order_by('Class_Amount')
    return render(request, 'filter/fee_amount_dropdown_list_options.html', {'fee_amounts': fee_amounts})


# function for loading discount of a student
def load_student_discount(request):
    student_id = request.GET.get('student')
    discs = Student.objects.filter(id=student_id).order_by('fees_discount')
    return render(request, 'filter/student_discount.html', {'discs': discs})


def load_sections(request):
    classroom_id = request.GET.get('classroom')
    sections = Section.objects.filter(classroom_id=classroom_id).order_by('section')
    return render(request, 'filter/section_dropdown_list_options.html', {'sections': sections})


def load_students(request):
    classroom_id = request.GET.get('classroom')
    students = Student.objects.filter(classroom_id=classroom_id).order_by('user')
    return render(request, 'filter/student_dropdown_list_options.html', {'students': students})


def load_roles(request):
    school_id = request.GET.get('school')
    roles = Role.objects.filter(school_id=school_id).order_by('role_name')
    return render(request, 'filter/role_dropdown_list_options.html', {'roles': roles})


def load_users(request):
    role_id = request.GET.get('user_type')
    users = User.objects.filter(roles_id=role_id).order_by('full_name')
    return render(request, 'filter/users_dropdown_list_options.html', {'users': users})


def load_payment_to(request):
    role_id = request.GET.get('role_type')
    payment_to = User.objects.filter(roles_id=role_id).order_by('full_name')
    return render(request, 'filter/payment_to_dropdown_list_options.html', {'payment_to': payment_to})


def load_payees(request):
    role_id = request.GET.get('role_type')
    payees = User.objects.filter(roles_id=role_id).order_by('full_name')
    return render(request, 'filter/payees_dropdown_list_options.html', {'payees': payees})


def load_user(request):
    role_id = request.GET.get('role')
    user = User.objects.filter(roles_id=role_id).order_by('full_name')
    return render(request, 'filter/user_dropdown_list_options.html', {'user': user})


def load_userz(request):
    role_id = request.GET.get('applicant_type')
    user = User.objects.filter(roles_id=role_id).order_by('full_name')
    return render(request, 'filter/user_dropdown_list_options.html', {'user': user})


def load_subjects(request):
    classroom_id = request.GET.get('classroom')
    subjects = Subject.objects.filter(classroom_id=classroom_id).order_by('subject_name')
    return render(request, 'filter/subject_dropdown_list_options.html', {'subjects': subjects})
