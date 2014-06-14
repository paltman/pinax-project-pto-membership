from django import forms

from .models import Contact, Student


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = [
            "first_name",
            "last_name",
            "email",
            "address_1",
            "address_2",
            "city",
            "zip_code",
            "cell_phone",
            "home_phone"
        ]


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            "grade",
            "teacher",
            "first_name",
            "last_name"
        ]
