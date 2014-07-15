from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView, CreateView, ListView, UpdateView

from django.contrib import messages

import stripe

from account.decorators import login_required
from account.mixins import LoginRequiredMixin

from .forms import ContactForm, StudentForm
from .models import Contact, SchoolYear, Student


def home(request):
    if request.user.is_authenticated():
        return redirect("memberships")
    return render(request, "homepage.html", {})


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


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact

    def get_queryset(self):
        return self.request.user.family.contacts.all().order_by("pk")

    def get_success_url(self):
        return reverse("contacts")


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student

    def get_queryset(self):
        return self.request.user.family.students.all().order_by("pk")

    def get_success_url(self):
        return reverse("students")


@require_POST
@login_required
def charge(request, pk):
    school_year = get_object_or_404(SchoolYear, pk=pk)
    token = request.POST.get("stripeToken")
    if token:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            charge_response = stripe.Charge.create(
                amount=school_year.amount,
                currency="usd",
                receipt_email=request.user.email,
                metadata={
                    "email": request.user.email,
                    "user_id": request.user.pk
                },
                card=token,
                description="{{ project_name }} Membership for the {0} school year.".format(school_year.year)
            )
            school_year.memberships.create(family=request.user.family, charge_id=charge_response["id"])
            messages.info(request, "Successfully charged card. Thanks for supporting the {{ project_name }}!")
        except stripe.CardError as e:
            messages.error(request, "There was an error with your card: {0}".format(e))
    return redirect("memberships")


class SchoolYearList(LoginRequiredMixin, ListView):
    model = SchoolYear

    def get_context_data(self, **kwargs):
        context = super(SchoolYearList, self).get_context_data(**kwargs)
        context.update({
            "current_year": SchoolYear.objects.get(active=True),
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context

    def get_queryset(self):
        return SchoolYear.objects.filter(active=False).order_by("-year")
