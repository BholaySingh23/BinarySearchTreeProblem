import re

class BookNode:
    def __init__(self, book_id, title, author, isbn):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True
        self.times_borrowed = 0
        self.left = None
        self.right = None
 
class PatronNode:
    def __init__(self, patron_id, name):
        self.patron_id = patron_id
        self.name = name
        self.borrowed_books = []
        self.left = None
        self.right = None
 
class BookLender:
    def __init__(self):
        self.book_root = None
        self.patron_root = None
 
    def _add_book_rec(self, node, book_id, title, author, isbn):
        if node is None:
            return BookNode(book_id, title, author, isbn)
        if book_id < node.book_id:
            node.left = self._add_book_rec(node.left, book_id, title, author, isbn)
        elif book_id > node.book_id:
            node.right = self._add_book_rec(node.right, book_id, title, author, isbn)
        else:
            node.title = title
            node.author = author
            node.isbn = isbn
        return node
 
    def add_book(self, book_id, title, author, isbn):
        self.book_root = self._add_book_rec(self.book_root, book_id, title, author, isbn)
        return f'Added Book: {book_id} - "{title}" by {author}, ISBN: {isbn}'
 
    def _search_book(self, node, book_id):
        if node is None or node.book_id == book_id:
            return node
        if book_id < node.book_id:
            return self._search_book(node.left, book_id)
        return self._search_book(node.right, book_id)
 
    def _list_available_books(self, node, available_books):
        if node:
            self._list_available_books(node.left, available_books)
            if node.available:
                available_books.append(f'- Book ID {node.book_id}: "{node.title}" by {node.author}')
            self._list_available_books(node.right, available_books)
 
    def list_available_books(self):
        available_books = []
        self._list_available_books(self.book_root, available_books)
        return "Available Books:\n" + "\n".join(available_books)
 
    def _list_books_by_author(self, node, author_name, books_by_author):
        if node is None:
            return
        self._list_books_by_author(node.left, author_name, books_by_author)
        if node.author.strip().lower() == author_name.strip().lower():
            books_by_author.append(f'- Book ID {node.book_id}: "{node.title}" by {node.author}')
        self._list_books_by_author(node.right, author_name, books_by_author)
 
    def list_books_by_author(self, author_name):
        books_by_author = []
        self._list_books_by_author(self.book_root, author_name, books_by_author)
        if books_by_author:
            return f'Books by Author "{author_name}":\n' + "\n".join(books_by_author)
        else:
            return f'No books found by Author "{author_name}".'
 
    def borrow_book(self, book_id, patron_id):
        book = self._search_book(self.book_root, book_id)
        if book is None or not book.available:
            return f'Book ID {book_id} is not available for borrowing.'
        patron = self.search_patron(self.patron_root, patron_id)
        if patron is None:
            self.patron_root = self._add_pateron(self.patron_root, patron_id, f'Patron {patron_id}')
            patron = self.search_patron(self.patron_root, patron_id)
        book.available = False
        book.times_borrowed += 1
        patron.borrowed_books.append(book_id)
        return f'Patron {patron_id} borrowed "{book.title}" (Book ID: {book_id})'
 
    def check_book(self, book_id):
        book = self._search_book(self.book_root, book_id)
        if book is None:
            return f'Book Details for ID {book_id}'
        if book.available:
            return f'Book Details for ID {book_id} :\n - {book.title} by {book.author}, ISBN: {book.isbn}, Available: Yes'
        return f'Book Details for ID {book_id} : \n- {book.title} by {book.author}, ISBN: {book.isbn}, Available: No'
    
    def _add_pateron(self, node, patron_id, name):
        if node is None:
            return PatronNode(patron_id, name)
        if patron_id < node.patron_id:
            node.left = self._add_pateron(node.left, patron_id, name)
        elif patron_id > node.patron_id:
            node.right = self._add_pateron(node.right, patron_id, name)
        return node
 
    def search_patron(self, node, patron_id):
        if node is None or node.patron_id == patron_id:
            return node
        if patron_id < node.patron_id:
            return self.search_patron(node.left, patron_id)
        return self.search_patron(node.right, patron_id)
 
    def return_book(self, book_id, patron_id):
        book = self._search_book(self.book_root, book_id)
        if book is None or book.available:
            return f'Book ID {book_id} is not currently borrowed.'
        patron = self.search_patron(self.patron_root, patron_id)
        if patron is None or book_id not in patron.borrowed_books:
            return f'Patron {patron_id} did not borrow Book ID {book_id}.'
        book.available = True
        patron.borrowed_books.remove(book_id)
        return f'Patron {patron_id} returned "{book.title}" (Book ID: {book_id})'
 
    def list_patrons_books(self, patron_id):
        patron = self.search_patron(self.patron_root, patron_id)
        if patron is None or not patron.borrowed_books:
            return f'Patron {patron_id} has not borrowed any books.'
        borrowed_books = []
        for book_id in patron.borrowed_books:
            book = self._search_book(self.book_root, book_id)
            borrowed_books.append(f'- "{book.title}" (Book ID: {book_id})')
        return f'Patron {patron_id} borrowed the following books:\n' + "\n".join(borrowed_books)


if __name__ == "__main__":
    library = BookLender()

    # File processing logic directly included in the main block
    input_file = 'inputPS04.txt'
    output_file = 'outputPS04.txt'

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            command = line.strip()
            if re.match(r"^addBook:", command):
                _, details = command.split(":", 1)
                book_id, title, author, isbn = map(str.strip, details.split(","))
                result = library.add_book(int(book_id), title.strip('"'), author.strip('"'), isbn.strip('"'))
            elif re.match(r"^borrowBook:", command):
                _, details = command.split(":", 1)
                book_id, patron_id = map(int, details.split(","))
                result = library.borrow_book(book_id, patron_id)
            elif re.match(r"^returnBook:", command):
                _, details = command.split(":", 1)
                book_id, patron_id = map(int, details.split(","))
                result = library.return_book(book_id, patron_id)
            elif re.match(r"^checkBook:", command):
                _, book_id = command.split(":", 1)
                result = library.check_book(int(book_id))
            elif re.match(r"^listAvailableBooks", command):
                result = library.list_available_books()
            elif re.match(r"^listBooksByAuthor:", command):
                _, author_name = command.split(":", 1)
                result = library.list_books_by_author(author_name.strip('"'))
            elif re.match(r"^listPatronsBooks:", command):
                _, patron_id = command.split(":", 1)
                result = library.list_patrons_books(int(patron_id))
            outfile.write(result + "\n")
