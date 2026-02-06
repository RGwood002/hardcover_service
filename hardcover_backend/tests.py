from django.test import TestCase
from rest_framework.test import APITestCase
# Create your tests here.

class InsertBookTestSuccess(APITestCase):
    def test_insert_book_success(self):
        response = self.client.post('/api/insert-book',data={"isbn" : "9780593820247"}, format='json')

        self.assertEqual(response.status_code, 200)
    
    def test_insert_book_fail_isbn_not_found(self):
        response = self.client.post('/api/insert-book', data={"isbn" : "9780593820247796909"})

        self.assertEqual(response.status_code, 404)
