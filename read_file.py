class BookNode:
    def __init__(self, bookId, title, author, isbn):
        self.bookId = bookId
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True
        self.timesBorrowed = 0
        self.left = None
        self.right = None
 
class PatronNode:
    def __init__(self, patronId, name):
        self.patronId = patronId
        self.name = name
        self.borrowedBooks = []
        self.left = None
        self.right = None
 
class LibraryManagement:
    def __init__(self):
        self.bookRoot = None
        self.patronRoot = None
 
    # Helper function to add a book to the BST
    def addBookRec(self, pNode, bookId, title, author, isbn):
        if pNode is None:
            return BookNode(bookId, title, author, isbn)
        if bookId < pNode.bookId:
            pNode.left = self.addBookRec(pNode.left, bookId, title, author, isbn)
        elif bookId > pNode.bookId:
            pNode.right = self.addBookRec(pNode.right, bookId, title, author, isbn)
        else:
            pNode.title = title
            pNode.author = author
            pNode.isbn = isbn
        return pNode
 
    # Add a book
    def addBook(self, bookId, title, author, isbn):
        self.bookRoot = self.addBookRec(self.bookRoot, bookId, title, author, isbn)
        return f'Added Book: {bookId} - "{title}" by {author}, ISBN: {isbn}'
 
    # Helper function to search for a book
    def searchBook(self, pNode, bookId):
        if pNode is None or pNode.bookId == bookId:
            return pNode
        if bookId < pNode.bookId:
            return self.searchBook(pNode.left, bookId)
        return self.searchBook(pNode.right, bookId)
 
    # Helper function to list available books
    def listAvailableBooksRec(self, pNode, availableBooks):
        if pNode:
            self.listAvailableBooksRec(pNode.left, availableBooks)
            if pNode.available:
                availableBooks.append(f'- Book ID {pNode.bookId}: "{pNode.title}" by {pNode.author}')
            self.listAvailableBooksRec(pNode.right, availableBooks)
 
    def listAvailableBooks(self):
        availableBooks = []
        self.listAvailableBooksRec(self.bookRoot, availableBooks)
        return "Available Books:\n" + "\n".join(availableBooks)
 
    # Helper function to find books by author
    def listBooksByAuthorRec(self, pNode, authorName, booksByAuthor):
        if pNode is None:
            return
        # Traverse the left subtree
        self.listBooksByAuthorRec(pNode.left, authorName, booksByAuthor)
        # Compare author names (case-insensitive and trimmed)
        if pNode.author.strip().lower() == authorName.strip().lower():
            booksByAuthor.append(f'- Book ID {pNode.bookId}: "{pNode.title}" by {pNode.author}')
        # Traverse the right subtree
        self.listBooksByAuthorRec(pNode.right, authorName, booksByAuthor)
 
 
    def listBooksByAuthor(self, authorName):
        booksByAuthor = []
        self.listBooksByAuthorRec(self.bookRoot, authorName, booksByAuthor)
        if booksByAuthor:
            return f'Books by Author "{authorName}":\n' + "\n".join(booksByAuthor)
        else:
            return f'No books found by Author "{authorName}".'
 
    # Borrow a book
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
        return f'Patron {patronId} borrowed "{book.title}" (Book ID: {bookId})'
    #Helper function for checkBook
    def checkBook(self, bookId):
        book = self.searchBook(self.bookRoot, bookId)
        if book is None :
            return f'Book Details for ID {bookId}'
        if book.available:
            return f'Book Details for ID {bookId} :\n - {book.title} by {book.author}, ISBN: {book.isbn}, Available: Yes'
        return f'Book Details for ID {bookId} : \n- {book.title} by {book.author}, ISBN: {book.isbn}, Available: No'
    
    # Helper function to add a patron to the BST
    def addPatronRec(self, pNode, patronId, name):
        if pNode is None:
            return PatronNode(patronId, name)
        if patronId < pNode.patronId:
            pNode.left = self.addPatronRec(pNode.left, patronId, name)
        elif patronId > pNode.patronId:
            pNode.right = self.addPatronRec(pNode.right, patronId, name)
        return pNode
 
    # Helper function to search for a patron
    def searchPatron(self, pNode, patronId):
        if pNode is None or pNode.patronId == patronId:
            return pNode
        if patronId < pNode.patronId:
            return self.searchPatron(pNode.left, patronId)
        return self.searchPatron(pNode.right, patronId)
 
    # Return a book
    def returnBook(self, bookId, patronId):
        book = self.searchBook(self.bookRoot, bookId)
        if book is None or book.available:
            return f'Book ID {bookId} is not currently borrowed.'
        patron = self.searchPatron(self.patronRoot, patronId)
        if patron is None or bookId not in patron.borrowedBooks:
            return f'Patron {patronId} did not borrow Book ID {bookId}.'
        book.available = True
        patron.borrowedBooks.remove(bookId)
        return f'Patron {patronId} returned "{book.title}" (Book ID: {bookId})'
 
    # List books borrowed by a patron
    def listPatronsBooks(self, patronId):
        patron = self.searchPatron(self.patronRoot, patronId)
        if patron is None or not patron.borrowedBooks:
            return f'Patron {patronId} has not borrowed any books.'
        borrowedBooks = []
        for bookId in patron.borrowedBooks:
            book = self.searchBook(self.bookRoot, bookId)
            borrowedBooks.append(f'- "{book.title}" (Book ID: {bookId})')
        return f'Patron {patronId} borrowed the following books:\n' + "\n".join(borrowedBooks)
 
    # Process input commands
    def processFile(self, input_file, output_file):
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                command = line.strip()
                if command.startswith("addBook:"):
                    _, details = command.split(":", 1)
                    bookId, title, author, isbn = map(str.strip, details.split(","))
                    result = self.addBook(int(bookId), title.strip('"'), author.strip('"'), isbn.strip('"'))
                elif command.startswith("borrowBook:"):
                    _, details = command.split(":", 1)
                    bookId, patronId = map(int, details.split(","))
                    result = self.borrowBook(bookId, patronId)
                elif command.startswith("returnBook:"):
                    _, details = command.split(":", 1)
                    bookId, patronId = map(int, details.split(","))
                    result = self.returnBook(bookId, patronId)
                elif command.startswith("checkBook:"):
                    _, bookId = command.split(":", 1)
                    result = self.checkBook(int(bookId))
                elif command.startswith("listAvailableBooks"):
                    result = self.listAvailableBooks()
                elif command.startswith("listBooksByAuthor:"):
                    _, authorName = command.split(":", 1)
                    result = self.listBooksByAuthor(authorName.strip().strip('"'))
                elif command.startswith("listPatronsBooks:"):
                    _, patronId = command.split(":", 1)
                    result = self.listPatronsBooks(int(patronId))
                outfile.write(result + "\n")

if __name__ == "__main__":
    library = LibraryManagement()
    library.processFile('inputPS04.txt', 'outputPS04.txt')
 