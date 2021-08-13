from enum import Enum
from rest_framework.pagination import PageNumberPagination


def is_authenticated(request):
    """ whether or not request user is authenticated or not """
    return request.user and request.user.is_authenticated


class DynamicPagination(PageNumberPagination):
    """ pagination class for returning paginated response """
    page_size = 25
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ChoiceBase(Enum):
    """ base class for model choice fields as Enum """

    @classmethod
    def to_list(cls):
        """ return a list of (name, value) which can be used as choice field in models"""
        return [(d.value, d.name) for d in cls]


class AuditVerbEnum(ChoiceBase):
    CREATED = 'C'
    UPDATED = 'U'
    DELETED = 'D'


def backoff(attempts):
    """Return a backoff delay, in seconds, given a number of attempts.

    The delay increases very rapidly with the number of attempts:
    1, 2, 4, 8, 16, 32, ... seconds

    """
    return 2 ** attempts
