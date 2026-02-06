from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from .models import  CheckInBook
from .serializers import  CheckInBookSerializer
from .hardcover_exceptions import FailedToGetBookInfo, FailedToInsertUserBook
from .external_api.graphql_client import client, gql, get_book_info, get_book_info_by_isbn, insert_user_book
import logging

logger = logging.getLogger(__name__)

# Create your views here.
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def insert_book_by_isbn(request: Request):
    logger.info(request)
    isbn = request.data.get('isbn')
    try:
        book_info = get_book_info_by_isbn(isbn)
    except FailedToGetBookInfo as e:
        error_mess = f"Failed to find book with ISBN: {e.isbn}"
        logger.error(error_mess)
        data = {"error": error_mess}
        
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    logger.info(isbn)
    
    book_id = book_info["editions"][0]["book_id"]
    book_edition_id = book_info["editions"][0]["id"]
    logger.info(book_id)

    try:
        insert_book = insert_user_book(book_id, book_edition_id) 
        logger.info(insert_book)
    except FailedToInsertUserBook as e:
        book = book(e.hardcover_error)
        data = {"error": f"Failed to insert book_id: {book_id} with edition_id: {book_edition_id} might have an issue"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    else:
        book_to_insert = CheckInBook(book_info, isbn)
        serializer = CheckInBookSerializer(book_to_insert, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
 