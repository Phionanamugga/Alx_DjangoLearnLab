from relationship_app.models import Author, Book, Library, Librarian

# Query 1: All books by a specific author
author_name = "Chinua Achebe"
try:
    author = Author.objects.get(name=author_name)
    books_by_author = author.books.all()
    print(f"Books by {author.name}: {[book.title for book in books_by_author]}")
except Author.DoesNotExist:
    print(f"No author found with name {author_name}")

# Query 2: List all books in a library
library_name = "Main City Library"
try:
    library = Library.objects.get(name=library_name)
    books_in_library = library.books.all()
    print(f"Books in {library.name}: {[book.title for book in books_in_library]}")
except Library.DoesNotExist:
    print(f"No library found with name {library_name}")

# Query 3: Retrieve the librarian for a library
try:
    library = Library.objects.get(name=library_name)
    librarian = library.librarian
    print(f"Librarian for {library.name}: {librarian.name}")
except Library.DoesNotExist:
    print(f"No library found with name {library_name}")
except Librarian.DoesNotExist:
    print(f"No librarian assigned to {library.name}")
