from rest_framework.pagination import PageNumberPagination

class NumberPagination(PageNumberPagination):
    
    page_size = 5
    max_page_size= 6
    page_query_param = 'Pg'
    page_size_query_param="Rg"