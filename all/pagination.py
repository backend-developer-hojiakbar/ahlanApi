from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10  # Har sahifada 10 ta element
    page_size_query_param = 'page_size'  # Foydalanuvchi o‘zi sozlashi mumkin
    max_page_size = 100  # Maksimal sahifa hajmi