from django.db import models
import datetime
from django.utils import timezone
# Create your models here.
class CheckInBook(models.Model):
    isbn = models.CharField(max_length=13)
    book_id = models.CharField(max_length=100)
    title = models.CharField(max_length=300)
    edition_format = models.CharField(max_length=30)
    edition_id = models.CharField(max_length=20)
    insert_dt = models.DateField()


    def __init__(self, get_by_isbn_response, isbn):
        self.isbn = isbn
        self.book_id = get_by_isbn_response["editions"][0]["book_id"]
        self.title = get_by_isbn_response["editions"][0]["title"]
        self.edition_format = get_by_isbn_response["editions"][0]["edition_format"]
        self.edition_id = get_by_isbn_response["editions"][0]["id"]
        self.insert_dt = timezone.now()  
