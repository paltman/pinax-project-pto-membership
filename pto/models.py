from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from localflavor.us import models as us
from localflavor.us.us_states import STATE_CHOICES as ORIGINAL_STATE_CHOICES


STATE_CHOICES = [(x[0], x[0]) for x in ORIGINAL_STATE_CHOICES]


class SchoolYear(models.Model):

    year = models.CharField(max_length=20, unique=True)
    dues = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)

    @property
    def amount(self):
        return int(self.dues * 100)

    def __unicode__(self):
        return "{2}{0} (${1})".format(self.year, self.dues, "* " if self.active else "")

    def membership_count(self):
        return self.memberships.count()

    def save(self, *args, **kwargs):
        if self.active:
            SchoolYear.objects.all().update(active=False)
        return super(SchoolYear, self).save(*args, **kwargs)


class Family(models.Model):

    user = models.OneToOneField(User, null=True, blank=True)
    name = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name_plural = "families"

    def __unicode__(self):
        return self.user.username if self.user is not None else self.name

    def clean(self):
        super(Family, self).clean()
        if self.user is None and len(self.name) == 0:
            raise ValidationError("If setting up manually, a family name must be supplied.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Family, self).save(*args, **kwargs)


class Membership(models.Model):

    family = models.ForeignKey(Family, related_name="memberships")
    school_year = models.ForeignKey(SchoolYear, related_name="memberships")
    charge_id = models.CharField(max_length=150)
    paid_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = [("family", "school_year")]


class Grade(models.Model):

    grade = models.CharField(max_length=2, unique=True)
    label = models.CharField(max_length=30)

    def __unicode__(self):
        return self.label

    def student_count(self):
        return self.students.count()


class Teacher(models.Model):

    grade = models.ForeignKey(Grade, related_name="teachers")
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)

    def __unicode__(self):
        return "{0}, {1} ({2})".format(self.last_name, self.first_name, self.grade)

    class Meta:
        unique_together = [("grade", "first_name", "last_name")]

    def student_count(self):
        return self.students.count()


class Contact(models.Model):

    family = models.ForeignKey(Family, related_name="contacts")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    address_1 = models.CharField(max_length=50, blank=True)
    address_2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=2, default="TN", choices=STATE_CHOICES)
    zip_code = models.CharField(max_length=50, blank=True)
    cell_phone = us.PhoneNumberField(blank=True)
    home_phone = us.PhoneNumberField(blank=True)

    def __unicode__(self):
        return "{0}, {1}".format(self.last_name, self.first_name)


class Student(models.Model):

    family = models.ForeignKey(Family, related_name="students")
    grade = models.ForeignKey(Grade, related_name="students")
    teacher = models.ForeignKey(Teacher, related_name="students")
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)

    def __unicode__(self):
        return "{0}, {1} ({2})".format(self.last_name, self.first_name, self.grade)
