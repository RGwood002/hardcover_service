from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from ..hardcover_exceptions import FailedToGetBookInfo, FailedToInsertUserBook
import logging

logger = logging.getLogger(__name__)
bearer_token = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJIYXJkY292ZXIiLCJ2ZXJzaW9uIjoiOCIsImp0aSI6IjA0NjRmYzJiLTY4ODEtNDZlYS1iYWQ3LTQ0MThiN2IzMDJjNCIsImFwcGxpY2F0aW9uSWQiOjIsInN1YiI6IjY2NDM1IiwiYXVkIjoiMSIsImlkIjoiNjY0MzUiLCJsb2dnZWRJbiI6dHJ1ZSwiaWF0IjoxNzY5MjkxMTAwLCJleHAiOjE4MDA4MjcxMDAsImh0dHBzOi8vaGFzdXJhLmlvL2p3dC9jbGFpbXMiOnsieC1oYXN1cmEtYWxsb3dlZC1yb2xlcyI6WyJ1c2VyIl0sIngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6InVzZXIiLCJ4LWhhc3VyYS1yb2xlIjoidXNlciIsIlgtaGFzdXJhLXVzZXItaWQiOiI2NjQzNSJ9LCJ1c2VyIjp7ImlkIjo2NjQzNX19.fqIP2gn-SAqScWBAzAD8AvLMt6ayVhI8hnArr9Xf-nA"

transport = RequestsHTTPTransport(
    url="https://api.hardcover.app/v1/graphql",
    headers={"Authorization": bearer_token}
)

client = Client(transport=transport, fetch_schema_from_transport=False)

def get_book_info(title):
    query = gql(f"""
                    {{
        books(where: {{title : {{_eq: "{title}"}}}}){{
            title,
            pages
        }}
    }}
                    """)
    logger.info(f"{bearer_token}")
    logger.info(query)
    result = client.execute(query)

    return result

def get_book_info_by_isbn(isbn):
    isbn_field = "isbn_13"  if len(isbn) > 10 else "isbn_10"
    query = gql(f"""
             {{
    editions(where: {{{isbn_field}: {{_eq: "{isbn}"}}}}){{
        book_id
        title
        edition_format
        id
    }}
}}
             """)
    try:
        result = client.execute(query)
        logger.info(result)
        if result['editions']:
            return result
        raise FailedToGetBookInfo(isbn)
    except Exception:
        raise FailedToGetBookInfo(isbn)


def insert_user_book(book_id, edition_id):
    query = gql(f"""
                mutation Insert_user_book {{
    insert_user_book(object: {{ 
                book_id: {book_id} 
                edition_id: {edition_id}}}) {{
        error
        id
    }}
}}
                """)
    
    try:
        result = client.execute(query)
        logger.info(result)
        error = result["insert_user_book"]["error"]
        return_id = result["insert_user_book"]["id"]
        if error is not None:
            raise FailedToInsertUserBook(book_id, error)
        return return_id
    except Exception:
        return FailedToInsertUserBook(book_id)