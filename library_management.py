# library_management_system.py

class BookNode:
    def __init__(self, bookId, title, author, isbn):
        self.bookId = bookId
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True  # Initially, the book is available
        self.borrowCount = 0  # Tracks how many times the book has been borrowed
        self.left = None
        self.right = None


class PatronNode:
    def __init__(self, patronId, name):
        self.patronId = patronId
        self.name = name
        self.borrowedBooks = []  # List of borrowed book IDs
        self.left = None
        self.right = None


class LibraryBST:
    def __init__(self):
        self.bookRoot = None
        self.patronRoot = None

    # --- Book Tree Operations ---
    def _addBookRec(self, pNode, bookId, title, author, isbn):
        if not pNode:
            return BookNode(bookId, title, author, isbn)

        if bookId < pNode.bookId:
            pNode.left = self._addBookRec(pNode.left, bookId, title, author, isbn)
        elif bookId > pNode.bookId:
            pNode.right = self._addBookRec(pNode.right, bookId, title, author, isbn)
        return pNode

    def addBook(self, bookId, title, author, isbn):
        self.bookRoot = self._addBookRec(self.bookRoot, bookId, title, author, isbn)
        return f'Added Book: {bookId}- "{title}" by {author}, ISBN: {isbn}'

    def _searchBook(self, pNode, bookId):
        if not pNode or pNode.bookId == bookId:
            return pNode
        if bookId < pNode.bookId:
            return self._searchBook(pNode.left, bookId)
        return self._searchBook(pNode.right, bookId)
    
    def borrowBook(self, bookId, patronId):
        book = self.searchBook(self.bookRoot, bookId)
        if book is None or not book.available:
            return f'Book ID {bookId} is not available for borrowing.'
        # Add patron if not already in system
        patron = self.searchPatron(self.patronRoot, patronId)
        if patron is None:
            self.patronRoot = self.addPatronRec(self.patronRoot, patronId, f'Patron {patronId}')
            patron = self.searchPatron(self.patronRoot, patronId)
        book.available = False
        book.timesBorrowed += 1
        patron.borrowedBooks.append(bookId)
        return f'Patron {patronId} borrowed "{book.title}" (Book ID: {bookId})'

    # def borrowBook(self, bookId, patronId):
    #     book = self._searchBook(self.bookRoot, bookId)
    #     patron = self._searchPatron(self.patronRoot, patronId)

    #     if not book:
    #         return f'Error: Book ID {bookId} not found.'
    #     if not patron:
    #         return f'Error: Patron ID {patronId} not found.'
    #     if not book.available:
    #         return f'Error: Book ID {bookId} is already borrowed.'

    #     book.available = False
    #     book.borrowCount += 1
    #     patron.borrowedBooks.append(bookId)
    #     return f'Patron {patronId} borrowed "{book.title}" (Book ID: {bookId})'

    def returnBook(self, bookId, patronId):
        book = self._searchBook(self.bookRoot, bookId)
        patron = self._searchPatron(self.patronRoot, patronId)

        if not book:
            return f'Error: Book ID {bookId} not found.'
        if not patron:
            return f'Error: Patron ID {patronId} not found.'
        if book.available:
            return f'Error: Book ID {bookId} is not currently borrowed.'

        book.available = True
        if bookId in patron.borrowedBooks:
            patron.borrowedBooks.remove(bookId)
        return f'Patron {patronId} returned "{book.title}" (Book ID: {bookId})'

    def _listAvailableBooks(self, pNode, availableBooks):
        if not pNode:
            return
        self._listAvailableBooks(pNode.left, availableBooks)
        if pNode.available:
            availableBooks.append(f'Book ID {pNode.bookId}: "{pNode.title}" by {pNode.author}')
        self._listAvailableBooks(pNode.right, availableBooks)

    def listAvailableBooks(self):
        availableBooks = []
        self._listAvailableBooks(self.bookRoot, availableBooks)
        return "Available Books:- " + " - ".join(availableBooks)

    def checkBook(self, bookId):
        book = self._searchBook(self.bookRoot, bookId)
        if not book:
            return f'Error: Book ID {bookId} not found.'
        availability = "Yes" if book.available else "No"
        return f'Book Details for ID {bookId}:- "{book.title}" by {book.author}, ISBN: {book.isbn}, Available: {availability}'

    # --- Patron Tree Operations ---
    def _addPatronRec(self, pNode, patronId, name):
        if not pNode:
            return PatronNode(patronId, name)

        if patronId < pNode.patronId:
            pNode.left = self._addPatronRec(pNode.left, patronId, name)
        elif patronId > pNode.patronId:
            pNode.right = self._addPatronRec(pNode.right, patronId, name)
        return pNode

    def addPatron(self, patronId, name):
        self.patronRoot = self._addPatronRec(self.patronRoot, patronId, name)
        return f'Added Patron: {patronId} - {name}'

    def _searchPatron(self, pNode, patronId):
        if not pNode or pNode.patronId == patronId:
            return pNode
        if patronId < pNode.patronId:
            return self._searchPatron(pNode.left, patronId)
        return self._searchPatron(pNode.right, patronId)

    def listPatronsBooks(self, patronId):
        patron = self._searchPatron(self.patronRoot, patronId)
        if not patron:
            return f'Error: Patron ID {patronId} not found.'
        if not patron.borrowedBooks:
            return f'Patron {patronId} has no borrowed books.'
        borrowedBooks = [
            f'"{self._searchBook(self.bookRoot, bookId).title}" (Book ID: {bookId})'
            for bookId in patron.borrowedBooks
        ]
        return f'Patron {patronId} borrowed the following books:- ' + ", ".join(borrowedBooks)


# Input Processing
def processInput(inputFile, outputFile):
    library = LibraryBST()
    with open(inputFile, 'r') as infile, open(outputFile, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if line.startswith('addBook'):
                _, data = line.split(': ', 1)
                bookId, title, author, isbn = eval(data)
                result = library.addBook(bookId, title, author, isbn)
                outfile.write(result + '\n')

            elif line.startswith('addPatron'):
                _, data = line.split(': ', 1)
                patronId, name = eval(data)
                result = library.addPatron(patronId, name)
                outfile.write(result + '\n')

            # elif line.startswith('borrowBook'):
            #     _, data = line.split(': ', 1)
            #     bookId, patronId = map(int, data.split(', '))
            #     result = library.borrowBook(bookId, patronId)
            #     outfile.write(result + '\n')
            elif line.startswith("borrowBook:"):
                _, details = line.split(":", 1)
                bookId, patronId = map(int, details.split(","))
                result = library.borrowBook(bookId, patronId)

            elif line.startswith('returnBook'):
                _, data = line.split(': ', 1)
                bookId, patronId = map(int, data.split(', '))
                result = library.returnBook(bookId, patronId)
                outfile.write(result + '\n')

            elif line.startswith('checkBook'):
                _, bookId = line.split(': ', 1)
                result = library.checkBook(int(bookId))
                outfile.write(result + '\n')

            elif line.startswith('listAvailableBooks'):
                result = library.listAvailableBooks()
                outfile.write(result + '\n')

            elif line.startswith('listPatronsBooks'):
                _, patronId = line.split(': ', 1)
                result = library.listPatronsBooks(int(patronId))
                outfile.write(result + '\n')


# Main Execution
if __name__ == "__main__":
    processInput('inputPS04.txt', 'outputPS04.txt')