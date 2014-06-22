from django import template

from ..models import Membership


register = template.Library()


@register.assignment_tag
def paid_at(school_year, user):
    try:
        return user.family.memberships.get(school_year=school_year).paid_at
    except Membership.DoesNotExist:
        return ""
