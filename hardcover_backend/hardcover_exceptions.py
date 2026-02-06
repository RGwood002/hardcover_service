class FailedToGetBookInfo(Exception):
    def __init__(self, isbn):
        self.isbn = isbn
        super().__init__(f"No book with ISBN: {isbn} was found")


class FailedToInsertUserBook(Exception):
    def __init__(self,book_id, hardcover_error):
        self.book_id = book_id
        self.hardcover_error = hardcover_error
        super().__init__(f"Failed to insert user book with book_id: {book_id}, due to {hardcover_error}")

    def __init__(self,book_id):
        self.book_id = book_id
        super().__init__(f"Failed to insert hardcover book with book_id: {book_id}")
