from relationship_app.models import Author, Book, Library, Librarian

# Create an Author
author = Author.objects.create(name="George Orwell")

# Create Books linked to the Author
book1 = Book.objects.create(title="1984", author=author)
book2 = Book.objects.create(title="Animal Farm", author=author)

# Create a Library and add Books
library = Library.objects.create(name="Central Library")
library.books.add(book1, book2)

# Create a Librarian linked to the Library
librarian = Librarian.objects.create(name="Jane Doe", library=library)

# Verify data
print(Author.objects.all())
print(Book.objects.all())
print(Library.objects.all())
print(Librarian.objects.all())