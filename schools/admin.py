from django.contrib import admin
from .models import *
from django.contrib.admin.models import LogEntry

# Register your models here.
admin.site.site_header = 'Welcome to M.S.M.S Administration Portal'


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name',
                    'national_ID',
                    'phone',
                    'gender',
                    'blood_group',
                    'religion',
                    'username',
                    'email',
                    'birth_date',
                    'other_info',
                    'photo',
                    ]


@admin.register(Superuser)
class SuperuserAdmin(admin.ModelAdmin):
    list_display = ['user', 'roles', 'resume']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'classroom', 'section', 'roll_no', 'admission_no')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['book_title',
                    'ISBN_no',
                    'edition',
                    'author',
                    'language',
                    'price',
                    'quantity',
                    'almira_no',
                    'book_cover'
                    ]


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ('user', 'roles', 'profession')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'designation', 'salary_type', 'resume', 'roles')


# @admin.register(Attendance)
# class StudentAttendanceAdmin(admin.ModelAdmin):
#     list_display = ('student', 'classroom', 'section', 'date')


@admin.register(TeacherAttendance)
class TeacherAttendanceAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'date')


@admin.register(EmployeeAttendance)
class EmployeeAttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date',)


@admin.register(Result)
class EmployeeAttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'classroom', 'term', 'year', 'gpa', 'cgpa')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "recipient", "timestamp")
    list_filter = ("sender", "recipient")


class AttendanceProfileAdmin(admin.ModelAdmin):
    list_display = ['student', 'classroom', 'date', 'status']


admin.site.register(Attendance, AttendanceProfileAdmin)

admin.site.register(LogEntry)
admin.site.register(Year)
admin.site.register(TakenSubject)
admin.site.register(Term)
admin.site.register(Settings)
admin.site.register(Subject)
admin.site.register(MonthlySalaryPaid)
admin.site.register(Routine)
admin.site.register(School)
admin.site.register(Classroom)
admin.site.register(Section)
admin.site.register(Teacher)
admin.site.register(Designation)
admin.site.register(BulkStudent)
admin.site.register(AbsentEmail)
admin.site.register(AbsentSMS)
admin.site.register(Exam)
admin.site.register(ExamSchedule)
admin.site.register(ExamSuggestion)
admin.site.register(ExamAttendance)
admin.site.register(Promotion)
admin.site.register(CertificateType)
admin.site.register(GenerateCertificate)
admin.site.register(LibraryMember)
admin.site.register(Issue)
admin.site.register(Vehicle)
admin.site.register(Route)
admin.site.register(TransportMember)
admin.site.register(Hostel)
admin.site.register(Room)
admin.site.register(HostelMember)
admin.site.register(Email)
admin.site.register(SMS)
admin.site.register(Notice)
admin.site.register(News)
admin.site.register(Holiday)
admin.site.register(Event)
admin.site.register(Visitor)
admin.site.register(SalaryGrade)
admin.site.register(Discounting)
admin.site.register(FeeType)
admin.site.register(Invoice)
admin.site.register(DueFeeEmail)
admin.site.register(DueFeeSMS)
admin.site.register(IncomeHead)
admin.site.register(Income)
admin.site.register(ExpenditureHead)
admin.site.register(Log)
admin.site.register(Purpose)
admin.site.register(Expenditure)
admin.site.register(Gallery)
admin.site.register(Image)
admin.site.register(Page)
admin.site.register(Slider)
admin.site.register(Role)
admin.site.register(Feedback)
admin.site.register(PaidDues)


class FeeTypeAdmin(admin.ModelAdmin):
    list_display = ('classamount',)


class DiscountingAdmin(admin.ModelAdmin):
    list_display = ('discountamount',)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('NetAmount', 'DueAmount', 'total_paid', 'updatestatus')


class PaidDuesAdmin(admin.ModelAdmin):
    list_display = ('deleting',)
