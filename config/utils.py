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
