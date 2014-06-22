from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, ListView, UpdateView

from .forms import ContactForm, StudentForm
from .models import Contact, Student


class ContactsView(ListView):
    model = Contact

    def get_queryset(self):
        return self.request.user.family.contacts.all().order_by("pk")


class StudentsView(TemplateView):
    template_name = "account/students.html"


class ContactCreateView(CreateView):
    form_class = ContactForm
    model = Contact

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.family = self.request.user.family
        self.object.save()
        return redirect("contacts")


class ContactUpdateView(UpdateView):
    form_class = ContactForm
    model = Contact

    def get_success_url(self):
        return reverse("contacts")


class StudentCreateView(CreateView):
    form_class = StudentForm
    model = Student

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.family = self.request.user.family
        self.object.save()
        return redirect("students")


class StudentUpdateView(UpdateView):
    form_class = StudentForm
    model = Student
    success_url = "students"
