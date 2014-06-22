from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView

from account.mixins import LoginRequiredMixin

from .forms import ContactForm, StudentForm
from .models import Contact, Student


class ContactsView(LoginRequiredMixin, ListView):
    model = Contact

    def get_queryset(self):
        return self.request.user.family.contacts.all().order_by("pk")


class StudentsView(LoginRequiredMixin, ListView):
    model = Student

    def get_queryset(self):
        return self.request.user.family.students.all().order_by("pk")


class ContactCreateView(LoginRequiredMixin, CreateView):
    form_class = ContactForm
    model = Contact

    def get_queryset(self):
        return self.request.user.family.contacts.all().order_by("pk")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.family = self.request.user.family
        self.object.save()
        return redirect("contacts")


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ContactForm
    model = Contact

    def get_queryset(self):
        return self.request.user.family.contacts.all().order_by("pk")

    def get_success_url(self):
        return reverse("contacts")


class StudentCreateView(LoginRequiredMixin, CreateView):
    form_class = StudentForm
    model = Student

    def get_queryset(self):
        return self.request.user.family.students.all().order_by("pk")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.family = self.request.user.family
        self.object.save()
        return redirect("students")


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    form_class = StudentForm
    model = Student

    def get_queryset(self):
        return self.request.user.family.students.all().order_by("pk")

    def get_success_url(self):
        return reverse("students")
