from django.contrib import admin

from .models import Grade, Teacher, Student, Contact, SchoolYear, Membership, Family


admin.site.register(
    Family,
    list_display=["user", "name"]
)
admin.site.register(
    SchoolYear,
    list_display=["year", "dues", "active", "membership_count"],
)
admin.site.register(
    Membership,
    list_display=["family", "school_year", "paid_at"],
    list_filter=["school_year", "paid_at"]
)
admin.site.register(
    Grade,
    readonly_fields=["grade"],
    list_display=["grade", "label", "student_count"],
    search_fields=["students__first_name", "students__last_name"]
)
admin.site.register(
    Teacher,
    list_display=["first_name", "last_name", "grade", "student_count"],
    search_fields=["first_name", "last_name", "students__first_name", "students__last_name"]
)
admin.site.register(
    Student,
    list_display=["first_name", "last_name", "grade", "teacher"],
    list_filter=["grade", "teacher"]
)
admin.site.register(
    Contact,
    list_display=["first_name", "last_name", "email", "address_1", "address_2", "city", "zip_code", "cell_phone", "home_phone"],
    search_fields=["first_name", "last_name", "email", "city", "zip_code", "cell_phone", "home_phone", "address_1", "address_2"],
    list_filter=["city"]
)
