from django import forms

from localflavor.us import forms as us

from .models import Contact, Student


class ContactForm(forms.ModelForm):

    zip_code = us.USZipCodeField(required=False)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = "First Name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Last Name"
        self.fields["address_1"].widget.attrs["placeholder"] = "Address Line 1"
        self.fields["address_2"].widget.attrs["placeholder"] = "Address Line 2"
        self.fields["city"].widget.attrs["placeholder"] = "City"
        self.fields["zip_code"].widget.attrs["placeholder"] = "Zip Code"
        self.fields["cell_phone"].widget.attrs["placeholder"] = "Cell Phone"
        self.fields["home_phone"].widget.attrs["placeholder"] = "Home Phone"
        self.fields["email"].widget.attrs["placeholder"] = "Email Address"

    class Meta:
        model = Contact
        fields = [
            "first_name",
            "last_name",
            "email",
            "address_1",
            "address_2",
            "city",
            "state",
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
